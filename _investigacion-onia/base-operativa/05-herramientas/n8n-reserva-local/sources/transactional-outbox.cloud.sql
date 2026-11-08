-- PostgreSQL >=13; especificación NO aplicada ni verificada con motor PostgreSQL.
CREATE SCHEMA IF NOT EXISTS onia_automation;
CREATE TABLE onia_automation.inbox (
 id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY, account text NOT NULL CHECK (btrim(account)<>''),
 event_id text NOT NULL CHECK (btrim(event_id)<>''), payload jsonb NOT NULL CHECK (jsonb_typeof(payload)='object'), UNIQUE(account,event_id));
CREATE TABLE onia_automation.outbox (
 inbox_id bigint PRIMARY KEY REFERENCES onia_automation.inbox(id), state text NOT NULL DEFAULT 'REVIEW_PENDING'
 CHECK (state IN ('REVIEW_PENDING','READY','CLAIMED','UNCERTAIN','DELIVERED','FAILED')),
 claim_token uuid, claimed_at timestamptz, attempts integer NOT NULL DEFAULT 0, provider_id text,
 CHECK (state<>'DELIVERED' OR NULLIF(btrim(provider_id),'') IS NOT NULL));
CREATE FUNCTION onia_automation.reserve(a text,e text,p jsonb) RETURNS bigint LANGUAGE plpgsql AS $$
DECLARE k bigint; prior jsonb;
BEGIN
 INSERT INTO onia_automation.inbox(account,event_id,payload) VALUES(a,e,p) ON CONFLICT(account,event_id) DO NOTHING RETURNING id INTO k;
 IF k IS NULL THEN
  SELECT id,payload INTO k,prior FROM onia_automation.inbox WHERE account=a AND event_id=e FOR UPDATE;
  IF prior IS DISTINCT FROM p THEN RAISE EXCEPTION 'event_payload_conflict'; END IF;
 END IF;
 INSERT INTO onia_automation.outbox(inbox_id) VALUES(k) ON CONFLICT DO NOTHING;
 RETURN k;
END $$;
CREATE FUNCTION onia_automation.claim() RETURNS SETOF onia_automation.outbox LANGUAGE sql AS $$
 WITH next AS (SELECT inbox_id FROM onia_automation.outbox WHERE state='READY' ORDER BY inbox_id LIMIT 1 FOR UPDATE SKIP LOCKED)
 UPDATE onia_automation.outbox o SET state='CLAIMED',claim_token=gen_random_uuid(),claimed_at=clock_timestamp(),attempts=o.attempts+1
 FROM next WHERE o.inbox_id=next.inbox_id RETURNING o.*;
$$;
CREATE FUNCTION onia_automation.complete(k bigint,t uuid,p text) RETURNS boolean LANGUAGE sql AS $$
 WITH done AS (UPDATE onia_automation.outbox SET state='DELIVERED',provider_id=p WHERE inbox_id=k AND claim_token=t
 AND state IN ('CLAIMED','UNCERTAIN') AND NULLIF(btrim(p),'') IS NOT NULL RETURNING 1) SELECT EXISTS(SELECT 1 FROM done);
$$;
