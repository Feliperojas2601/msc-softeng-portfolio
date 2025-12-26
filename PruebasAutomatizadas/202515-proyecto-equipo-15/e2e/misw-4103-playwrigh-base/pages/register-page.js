import { BasePage } from './base-page.js';
import { LoginPage } from './login-page.js';

export class RegisterPage extends BasePage {
    constructor(page, screenshotManager = null) {
        super(page, screenshotManager);
        this.createAccountButton = 'a.gh-btn-green';
        this.blogTitleInput = 'input[name="blog-title"]';
        this.nameInput = 'input[name="name"]';
        this.emailInput = 'input[name="email"]';
        this.passwordInput = 'input[name="password"]';
        this.createAccountSubmitButton = 'button.gh-btn-green';
        this.skipButton = 'button:has-text("I\'ll do this later")';
        this.alertMessage = 'div[class=gh-alert-content]';
    }

    async register(siteTitle = 'Test Blog', userName = 'Test User') {
        await this.executeWithScreenshot('register', async () => {
            const email = process.env.EMAIL;
            const password = process.env.PASSWORD;
            if (!email || !password) {
                throw new Error('EMAIL and PASSWORD environment variables must be set.');
            }
            await this.page.click(this.createAccountButton);
            await this.page.waitForTimeout(2000);
            await this.page.fill(this.blogTitleInput, siteTitle);
            await this.page.fill(this.nameInput, userName);
            await this.page.fill(this.emailInput, email);
            await this.page.fill(this.passwordInput, password);
            await this.page.waitForTimeout(1000);
            await this.page.click(this.createAccountSubmitButton);
            await this.page.waitForTimeout(3000);
            const alertLocator = this.page.locator(this.alertMessage);
            const hasAlert = await alertLocator.isVisible().catch(() => false);
            if (hasAlert) {
                const loginPage = new LoginPage(this.page, this.screenshotManager);
                await this.page.goto('/ghost/#/signin');
                await this.page.waitForLoadState('domcontentloaded');
                await loginPage.login();
                return;
            }
            const skipVisible = await this.page.locator(this.skipButton).isVisible().catch(() => false);
            if (skipVisible) {
                await this.page.click(this.skipButton);
                await this.page.waitForTimeout(2000);
            }
        });
    }
}
