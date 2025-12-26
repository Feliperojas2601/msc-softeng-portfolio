import { BasePage } from './base-page.js';

export class PagePage extends BasePage {
    constructor(page, screenshotManager = null) {
        super(page, screenshotManager);
        this.newPageButton = 'a[href="#/editor/page/"]';
        this.titleInput = 'textarea.gh-editor-title';
        this.contentInput = 'div.koenig-editor__editor';
        this.contentParagraph = 'div.koenig-editor__editor p';
        this.publishButton = 'div.gh-publishmenu-trigger';
        this.continueButton = 'button.gh-publishmenu-button';
        this.publishModal = '.publish-modal';
        this.rightNowButton = 'button[data-test-button="confirm-publish"]';
        this.closePublishFlowButton = 'a[href="#/pages/"]';
        this.pagesListItems = 'h3.gh-content-entry-title';
        this.featureImageButton = 'button.gh-editor-feature-image-add-button';
        this.featureImageInput = 'input[type="file"][accept*="image"]';
        this.imageCardButton = 'button[data-kg-card-menu-item="Image"]';
        this.plusButton = 'button[aria-label="Add a card"]';
        this.pageSelectorByTitle = (title) => `a.gh-post-list-title:has(h3.gh-content-entry-title:text-is("${title}"))`;
        this.featureImageSelector = 'div.gh-editor-feature-image img';
        this.settingsMenuButton = 'button[data-test-psm-trigger]';
        this.tagInputGeneric = 'input.ember-power-select-trigger-multiple-input';
        this.goBackToPagesButton = 'a[href="#/pages/"]';
        this.tagFilterButton = 'div[data-test-tag-select="true"] .ember-power-select-trigger';
        this.tagFilterOptionByName = (tagName) => `.ember-power-select-option:has-text("${tagName}")`;
        this.assignedTagsList = 'li.ember-power-select-multiple-option';
    }

    async clickOnNewPage() {
        await this.executeWithScreenshot('click_on_new_page', async () => {
            await this.page.click(this.newPageButton);
            await this.page.waitForTimeout(1000);
        });
    }

    async setPageTitle(title) {
        await this.executeWithScreenshot('set_page_title', async () => {
            await this.page.click(this.titleInput);
            await this.page.fill(this.titleInput, title);
            await this.page.waitForTimeout(500);
        });
    }

    async setPageContent(content) {
        await this.executeWithScreenshot('set_page_content', async () => {
            await this.page.click(this.contentInput);
            await this.page.waitForTimeout(500);
            await this.page.keyboard.type(content);
            await this.page.waitForTimeout(500);
        });
    }

    async clickOnPublishPage() {
        await this.executeWithScreenshot('click_on_publish_page', async () => {
            await this.page.click(this.publishButton);
            await this.page.waitForTimeout(1000);
        });
    }

    async clickOnContinueAfterPublish() {
        await this.executeWithScreenshot('click_on_continue_after_publish', async () => {
            await this.page.click(this.continueButton);
            await this.page.waitForTimeout(1000);
        });
    }

    async clickOnRightNowPublishPage() {
        await this.executeWithScreenshot('click_on_right_now_publish_page', async () => {
            await this.page.waitForTimeout(500);
        });
    }

    async clickOnClosePublishFlow() {
        await this.executeWithScreenshot('click_on_close_publish_flow', async () => {
            await this.page.click(this.closePublishFlowButton);
            await this.page.waitForTimeout(500);
        });
    }

    async getPublishedPagesTitles() {
        return await this.executeWithScreenshot('get_published_pages_titles', async () => {
            const titles = await this.page.$$eval(this.pagesListItems, elements =>
                elements.map(el => el.textContent.trim())
            );
            return titles;
        });
    }

    async setPageFeatureImage(imagePath) {
        await this.executeWithScreenshot('set_page_feature_image', async () => {
            await this.page.click(this.featureImageButton);
            await this.page.waitForTimeout(500);
            const imageInput = await this.page.locator(this.featureImageInput).last();
            await imageInput.setInputFiles(imagePath);
            await this.page.waitForTimeout(2000);
        });
    }

    async clickOnPageByTitle(title) {
        await this.executeWithScreenshot('click_on_page_by_title', async () => {
            const selector = this.pageSelectorByTitle(title);
            await this.page.waitForSelector(selector, { state: 'visible', timeout: 5000 });
            await this.page.click(selector);
            await this.page.waitForTimeout(2000);
        });
    }

    async getPageFeatureImageSrc() {
        return await this.executeWithScreenshot('get_page_feature_image_src', async () => {
            const src = await this.page.getAttribute(this.featureImageSelector, 'src');
            return src;
        });
    }

    async openPageSettings() {
        await this.executeWithScreenshot('open_page_settings', async () => {
            await this.page.click(this.settingsMenuButton);
            await this.page.waitForTimeout(1000);
        });
    }

    async assignTagToPage(tagName) {
        await this.executeWithScreenshot('assign_tag_to_page', async () => {
            await this.page.click(this.tagInputGeneric);
            await this.page.waitForTimeout(500);
            await this.page.keyboard.type(tagName);
            await this.page.waitForTimeout(500);
            await this.page.keyboard.press('Enter');
            await this.page.waitForTimeout(1000);
        });
    }

    async closePageSettings() {
        await this.executeWithScreenshot('close_page_settings', async () => {
            await this.page.click(this.settingsMenuButton);
            await this.page.waitForTimeout(1000);
        });
    }

    async clickOnGoBackToPages() {
        await this.executeWithScreenshot('click_on_go_back_to_pages', async () => {
            await this.page.click(this.goBackToPagesButton);
            await this.page.waitForTimeout(1000);
        });
    }

    async clickOnFilterPagesByTag(tagName) {
        await this.executeWithScreenshot('click_on_filter_pages_by_tag', async () => {
            await this.page.click(this.tagFilterButton);
            await this.page.waitForTimeout(500);
            const tagOption = this.tagFilterOptionByName(tagName);
            await this.page.click(tagOption);
            await this.page.waitForTimeout(1000);
        });
    }

    async getPageTags() {
        return await this.executeWithScreenshot('get_page_tags', async () => {
            const tags = await this.page.$$eval(this.assignedTagsList, elements =>
                elements.map(el => el.textContent.trim())
            );
            return tags.join(', ');
        });
    }
}