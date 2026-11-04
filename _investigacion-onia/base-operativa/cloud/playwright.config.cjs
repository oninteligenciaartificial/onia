const {defineConfig}=require('@playwright/test');
module.exports=defineConfig({testDir:'.',testMatch:'browser.spec.cjs',workers:1,reporter:'list',outputDir:'../operacion/cloud-002/playwright-results',use:{browserName:'chromium',headless:true,launchOptions:process.env.ONIA_CHROMIUM_PATH?{executablePath:process.env.ONIA_CHROMIUM_PATH}:{}}});
