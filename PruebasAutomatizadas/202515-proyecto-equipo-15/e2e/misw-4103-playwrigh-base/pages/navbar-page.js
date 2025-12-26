import { BasePage } from './base-page.js';

export class NavbarPage extends BasePage {
    constructor(page, screenshotManager = null) {
        super(page, screenshotManager);
        this.postsLink = 'a[href="#/posts/"]';
        this.pagesLink = 'a[href="#/pages/"]';
        this.pagesTagLink = 'a[href="#/tags/"]';
    }

    async clickOnPosts() {
        await this.executeWithScreenshot('click_on_posts', async () => {
            await this.page.waitForTimeout(2500);
            await this.page.click(this.postsLink);
        });
    }

    async clickOnPages() {
        await this.executeWithScreenshot('click_on_pages', async () => {
            await this.page.waitForTimeout(2500);
            await this.page.click(this.pagesLink);
        });
    }

    async clickOnTags() {
        await this.executeWithScreenshot('click_on_tags', async () => {
            await this.page.waitForTimeout(2500);
            await this.page.click(this.pagesTagLink);
        });
    }
}