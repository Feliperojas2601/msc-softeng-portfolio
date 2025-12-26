import { BasePage } from './base-page.js';

export class PagePage extends BasePage {
    constructor(page, screenshotManager = null) {
        super(page, screenshotManager);
        this.newPageButton = 'a[href="#/editor/page/"]';
        this.titleInput = 'textarea.gh-editor-title[placeholder="Page title"]';
        this.contentInput = 'div[data-lexical-editor="true"]';
        this.contentParagraph = 'div[data-lexical-editor="true"] p';
        this.publishButton = 'button[data-test-button="publish-flow"]';
        this.continueButton = 'button[data-test-button="continue"]';
        this.publishModal = '.publish-modal';
        this.rightNowButton = 'button[data-test-button="confirm-publish"]';
        this.closePublishFlowButton = 'button[data-test-button="close-publish-flow"]';
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
            await this.page.waitForSelector(this.titleInput, { state: 'visible' });
        });
    }

    async setPageTitle(title) {
        await this.executeWithScreenshot('set_page_title', async () => {
            await this.page.click(this.titleInput);
            await this.page.fill(this.titleInput, title);
        });
    }

    async setPageContent(content) {
        await this.executeWithScreenshot('set_page_content', async () => {
            await this.page.click(this.contentInput);
            await this.page.keyboard.type(content);
        });
    }

    async clickOnPublishPage() {
        await this.executeWithScreenshot('click_on_publish_page', async () => {
            await this.page.click(this.publishButton);
            await this.page.waitForSelector(this.continueButton, { state: 'visible' });
        });
    }

    async clickOnContinueAfterPublish() {
        await this.executeWithScreenshot('click_on_continue_after_publish', async () => {
            await this.page.click(this.continueButton);
            await this.page.waitForSelector(this.rightNowButton, { state: 'visible' });
        });
    }

    async clickOnRightNowPublishPage() {
        await this.executeWithScreenshot('click_on_right_now_publish_page', async () => {
            await this.page.click(this.rightNowButton, { force: true });
            await this.page.waitForSelector(this.closePublishFlowButton, { state: 'visible' });
        });
    }

    async clickOnClosePublishFlow() {
        await this.executeWithScreenshot('click_on_close_publish_flow', async () => {
            await this.page.click(this.closePublishFlowButton);
            await this.page.waitForSelector(this.pagesListItems, { state: 'visible' });
        });
    }

    async isPublishButtonVisible() {
        try {
            return await this.page.locator(this.publishButton).isVisible({ timeout: 3000 });
        } catch (error) {
            return false;
        }
    }

    async isPublishButtonEnabled() {
        try {
            const button = this.page.locator(this.publishButton);
            const isVisible = await button.isVisible({ timeout: 3000 });
            if (!isVisible) return false;
            return await button.isEnabled();
        } catch (error) {
            return false;
        }
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
            const imageInput = await this.page.locator(this.featureImageInput).last();
            await imageInput.setInputFiles(imagePath);
            await this.page.waitForSelector(this.featureImageSelector, { state: 'visible' });
        });
    }

    async clickOnPageByTitle(title) {
        await this.executeWithScreenshot('click_on_page_by_title', async () => {
            // Ensure we're on the pages list first
            await this.page.waitForSelector(this.pagesListItems, { state: 'visible', timeout: 10000 });
            
            const selector = this.pageSelectorByTitle(title);
            await this.page.waitForSelector(selector, { state: 'visible', timeout: 10000 });
            await this.page.click(selector);
            await this.page.waitForSelector(this.titleInput, { state: 'visible' });
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
            await this.page.waitForSelector(this.tagInputGeneric, { state: 'visible' });
        });
    }

    async assignTagToPage(tagName) {
        await this.executeWithScreenshot('assign_tag_to_page', async () => {
            await this.page.click(this.tagInputGeneric);
            await this.page.keyboard.type(tagName);
            
            // Wait for dropdown to appear
            await this.page.waitForSelector('.ember-power-select-dropdown', { state: 'visible', timeout: 3000 });
            
            // Small wait to ensure dropdown is fully loaded
            await this.page.waitForTimeout(500);
            
            // Press Enter to select/create the tag
            await this.page.keyboard.press('Enter');
            
            // Wait a bit for the tag to be processed
            await this.page.waitForTimeout(500);
            
            // Close the dropdown by pressing Escape (instead of waiting for it to auto-close)
            await this.page.keyboard.press('Escape');
            
            // Verify tag was added to the list
            const tagAdded = await this.page.locator(`li.ember-power-select-multiple-option`).filter({ hasText: tagName }).first();
            await tagAdded.waitFor({ state: 'visible', timeout: 5000 });
        });
    }

    async closePageSettings() {
        await this.executeWithScreenshot('close_page_settings', async () => {
            await this.page.click(this.settingsMenuButton);
            await this.page.waitForLoadState('networkidle');
        });
    }

    async clickOnGoBackToPages() {
        await this.executeWithScreenshot('click_on_go_back_to_pages', async () => {
            await this.page.click(this.goBackToPagesButton);
            await this.page.waitForSelector(this.pagesListItems, { state: 'visible' });
        });
    }

    async clickOnFilterPagesByTag(tagName) {
        await this.executeWithScreenshot('click_on_filter_pages_by_tag', async () => {
            await this.page.click(this.tagFilterButton);
            const tagOption = this.tagFilterOptionByName(tagName);
            await this.page.waitForSelector(tagOption, { state: 'visible' });
            await this.page.click(tagOption);
            await this.page.waitForLoadState('networkidle');
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