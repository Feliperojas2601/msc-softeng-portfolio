const fs = require('fs');
const { WebClient } = require('kraken-node');
const { After, AfterAll, Before, BeforeAll, BeforeStep } = require('@cucumber/cucumber');
const { ScreenshotManager } = require('./screenshot-manager');
const { faker } = require('@faker-js/faker');
const { hashString } = require('./utils');
const properties = require('../../../properties.json');

BeforeAll(async function () {
    console.log('Initial setting of the Kraken environment...');
});

Before(async function (scenario) {
  this.deviceClient = new WebClient('chrome', {}, this.userId);
  this.driver = await this.deviceClient.startKrakenForUserId(this.userId);
  console.log(`Starting scenario: ${scenario.pickle.name}`);

  const featureName = scenario.gherkinDocument?.feature?.name || 'unknown_feature';
  const scenarioName = scenario.pickle?.name || 'unknown_scenario';

  const scenarioHash = hashString(scenarioName);
  const baseSeed = parseInt(properties.FAKER_SEED || '42');
  const uniqueSeed = baseSeed + scenarioHash;
  faker.seed(uniqueSeed);
  console.log(`Faker initialized with seed: ${uniqueSeed}`);

  this.screenshotManager = new ScreenshotManager(this.driver, scenarioName, featureName);
  this.currentStepIndex = 0;

  // In case Driver exists
  await this.driver.setTimeout({
    implicit: 8000,
    pageLoad: 60000,
    script: 30000
  });

  await this.driver.pause(500);
});

After({timeout: 600000}, async function (scenario) {
  console.log(`Ended: ${scenario.pickle.name}`);

  try {
    if (scenario.result.status === 'FAILED') {
      const screenshot = await this.driver.takeScreenshot();
      const name = `./error-${Date.now()}.png`;
      fs.writeFileSync(name, screenshot, 'base64');
      console.log(`Screenshot saved: ${name}`);
    }
  } catch (e) {
    console.warn('Could not take screenshot:', e.message);
  }

  await this.deviceClient.stopKrakenForUserId(this.userId);
});

AfterAll(async function () {
  console.log('Ending test suite...');
});

BeforeStep(async function(step) {
    if (!this.screenshotManager) {
        console.warn('⚠️ ScreenshotManager not initialized');
        return;
    }
    try {
        const currentPickleStep = step.pickle?.steps?.[this.currentStepIndex];
        
        if (currentPickleStep?.text) {
            const stepText = currentPickleStep.text;
            console.log(`📸 Capturing screenshot for step ${this.currentStepIndex + 1}: ${stepText}`);
            await this.screenshotManager.captureStep(stepText);
            this.currentStepIndex++;
        } else {
            console.warn(`⚠️ Could not find step text for index ${this.currentStepIndex}`);
        }
    } catch (error) {
        console.warn(`⚠️ Error capturing screenshot:`, error.message);
    }
});