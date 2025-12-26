import { BasePage } from './base-page.js';

export class NavbarPage extends BasePage {
    constructor(page, screenshotManager = null) {
        super(page, screenshotManager);
        this.postsLink = 'a[data-test-nav="posts"]';
        this.pagesLink = 'a[data-test-nav="pages"]';
        this.pagesTagLink = 'a[data-test-nav="tags"]';
    }

    async clickOnPosts() {
        await this.executeWithScreenshot('click_on_posts', async () => {
            await this.page.click(this.postsLink);
            await this.page.waitForLoadState('networkidle');
        });
    }

    async clickOnPages() {
        await this.executeWithScreenshot('click_on_pages', async () => {
            await this.page.click(this.pagesLink);
            await this.page.waitForLoadState('networkidle');
        });
    }

    async clickOnTags() {
        await this.executeWithScreenshot('click_on_tags', async () => {
            await this.page.click(this.pagesTagLink);
            await this.page.waitForLoadState('networkidle');
        });
    }
}