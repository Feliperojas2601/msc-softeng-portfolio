import { BasePage } from './base-page.js';
import { LoginPage } from './login-page.js';

export class RegisterPage extends BasePage {
    constructor(page, screenshotManager = null) {
        super(page, screenshotManager);
        this.blogTitleInput = 'input[id="blog-title"]';
        this.nameInput = 'input[id="name"]';
        this.emailInput = 'input[id="email"]';
        this.passwordInput = 'input[id="password"]';
        this.registerButton = 'button[data-test-button="setup"]';
        this.alertMessage = 'div[class=gh-alert-content]';
    }

    async register(siteTitle = 'Test Blog', userName = 'Test User') {
        await this.executeWithScreenshot('register', async () => {
            const email = process.env.EMAIL;
            const password = process.env.PASSWORD;
            if (!email || !password) {
                throw new Error('EMAIL and PASSWORD environment variables must be set');
            }
            await this.page.fill(this.blogTitleInput, siteTitle);
            await this.page.fill(this.nameInput, userName);
            await this.page.fill(this.emailInput, email);
            await this.page.fill(this.passwordInput, password);
            await this.page.click(this.registerButton);
            await this.page.waitForLoadState('networkidle');
            const alertLocator = this.page.locator(this.alertMessage);
            const hasAlert = await alertLocator.isVisible().catch(() => false);
            if (hasAlert) {
                const loginPage = new LoginPage(this.page, this.screenshotManager);
                await this.page.goto('/ghost/#/signin');
                await this.page.waitForLoadState('domcontentloaded');
                await loginPage.login();
                return;
            }
        });
    }
}
