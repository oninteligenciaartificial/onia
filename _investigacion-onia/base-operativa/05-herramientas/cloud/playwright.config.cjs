const {defineConfig}=require('@playwright/test');
const {buildLaunchOptions}=require('./browser-runtime.cjs');
module.exports=defineConfig({testDir:'.',testMatch:'browser.spec.cjs',workers:1,reporter:'list',outputDir:'../operacion/cloud-002/playwright-results',use:{browserName:'chromium',headless:true,launchOptions:buildLaunchOptions()}});
