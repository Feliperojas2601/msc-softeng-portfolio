import { mkdirSync, existsSync } from 'node:fs';
import { join } from 'node:path';

export class ScreenshotManager {
    constructor(page, testInfo) {
        this.page = page;
        this.testInfo = testInfo;
        this.stepCounter = {};
        this.scenarioName = this.sanitizeFileName(testInfo.title);
        this.featureName = this.sanitizeFileName(testInfo.file.split('/').pop().replace('.spec.js', ''));
        this.screenshotsDir = join(
            process.cwd(), 
            'screenshots-vrt',
            this.featureName,
            this.scenarioName
        );
        this.ensureDirectoryExists();
    }

    sanitizeFileName(name) {
        return name
            .replaceAll(/[^a-z0-9]/gi, '_')
            .replaceAll(/_+/g, '_')
            .toLowerCase();
    }

    ensureDirectoryExists() {
        if (!existsSync(this.screenshotsDir)) {
            mkdirSync(this.screenshotsDir, { recursive: true });
        }
    }

    async captureStep(stepName) {
        const sanitizedStepName = this.sanitizeFileName(stepName);
        if (!this.stepCounter[sanitizedStepName]) {
            this.stepCounter[sanitizedStepName] = 1;
        } else {
            this.stepCounter[sanitizedStepName]++;
        }
        const counter = this.stepCounter[sanitizedStepName];
        const paddedCounter = String(counter).padStart(2, '0');
        const suffix = counter > 1 ? `_${paddedCounter}` : '';
        const filename = `step_${paddedCounter}_${sanitizedStepName}${suffix}.png`;
        const filepath = join(this.screenshotsDir, filename);
        await this.page.screenshot({ 
            path: filepath,
            fullPage: true 
        });
        return {
            path: filepath,
            stepName: sanitizedStepName,
            stepNumber: counter,
            scenario: this.scenarioName,
            feature: this.featureName
        };
    }

    async captureFinalStep() {
        const totalSteps = Object.values(this.stepCounter).reduce((a, b) => a + b, 0);
        const stepNumber = totalSteps + 1;
        return await this.captureStep(`final_step_${stepNumber}`);
    }
}