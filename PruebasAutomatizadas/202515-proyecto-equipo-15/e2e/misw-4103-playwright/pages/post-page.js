import { BasePage } from './base-page.js';
import { expect } from "@playwright/test";

export class PostPage extends BasePage {
    constructor(page, screenshotManager = null) {
        super(page, screenshotManager);
        this.newPostButton = 'a[href="#/editor/post/"]';
        this.titleInput = 'textarea.gh-editor-title[placeholder="Post title"]';
        this.contentInput = 'div[data-lexical-editor="true"]';
        this.contentParagraph = 'div[data-lexical-editor="true"] p';
        this.publishButton = 'button[data-test-button="publish-flow"]';
        this.continueButton = 'button[data-test-button="continue"]';
        this.publishModal = '.publish-modal';
        this.rightNowButton = 'button[data-test-button="confirm-publish"]';
        this.closePublishFlowButton = 'button[data-test-button="close-publish-flow"]';
        this.postsListItems = 'h3[class="gh-content-entry-title"]';
        this.featureImageButton = 'button.gh-editor-feature-image-add-button';
        this.featureImageInput = 'input[type="file"][accept*="image"]';
        this.imageCardButton = 'button[data-kg-card-menu-item="Image"]';
        this.plusButton = 'button[aria-label="Add a card"]';
        this.postSelectorByTitle = (title) => `a.gh-post-list-title:has(h3.gh-content-entry-title:text-is("${title}"))`;
        this.featureImageSelector = 'div.gh-editor-feature-image img';
        this.scheduleSettingButton = 'div.gh-publish-setting[data-test-setting="publish-at"] button.gh-publish-setting-title';
        this.scheduleForLaterLabel = 'div.gh-radio:has(div.gh-radio-button[data-test-radio="schedule"]) label';
        this.postStatusSelector = '.. >> p.gh-content-entry-status span';
        this.settingsMenuButton = 'button[data-test-psm-trigger]';
        this.tagInput = 'input#ember-power-select-trigger-multiple-input-ember427';
        this.tagInputGeneric = 'input.ember-power-select-trigger-multiple-input';
        this.goBackToPostsButton = 'a[href="#/posts/"]';
        this.assignedTagsList = 'li.ember-power-select-multiple-option';
        this.bodyContentInput = 'div[class="kg-prose"]';
        this.firstPost = 'a[class="ember-view permalink gh-list-data gh-post-list-title"]';
        this.updateButton = 'button[data-test-button="publish-save"]';
        this.postsButton = 'a[data-test-link="posts"]';
        this.imagePost = 'div[class="gh-editor-feature-image-overlay"]';
        this.deleteButton = 'button[class="image-action image-delete"]';
        this.settingsMenuButton = 'button[data-test-psm-trigger]';
        this.postHistoryButton = 'button[data-test-toggle="post-history"]';
        this.publishedVersionSelector = 'button[data-test-button="preview-revision"]';
        this.restoreButton = 'button[class="gh-post-history-version-restore"]';
        this.restorePostButton = 'button[data-test-button="restore"]';
        this.restoreBanner = 'div[data-test-modal="restore-revision"]';
        this.titleConfirmation = 'div[class="gh-editor-title"]';
        this.postDeleteButton = 'button[data-test-button="delete-post"]';
        this.pageLocator = 'li.gh-list-row.gh-posts-list-item';
        this.imageLocator = 'div.gh-editor-feature-image img';
        this.deleteBanner = 'div[class="modal-content"]';
        this.deletePostButton = 'button[data-test-button="delete-post-confirm"]';
        this.postRow = 'li.gh-list-row.gh-posts-list-item';
        this.postTitle = 'h3.gh-content-entry-title';
        this.postStatusSelector = 'p.gh-content-entry-status span';
    }

    async clickOnNewPost() {
        await this.executeWithScreenshot('click_on_new_post', async () => {
            await this.page.click(this.newPostButton);
            await this.page.waitForSelector(this.titleInput, { state: 'visible', timeout: 10000 });
        });
    }

    async setPostTitle(title) {
        await this.executeWithScreenshot('set_post_title', async () => {
            await this.page.fill(this.titleInput, title);
        });
    }

    async setPostContent(content) {
        await this.executeWithScreenshot('set_post_content', async () => {
            await this.page.click(this.contentInput);
            await this.page.keyboard.type(content);
        });
    }

    async clickOnPublishPost() {
        await this.executeWithScreenshot('click_on_publish_post', async () => {
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

    async clickOnRightNowPublishPost() {
        await this.executeWithScreenshot('click_on_right_now_publish_post', async () => {
            await this.page.click(this.rightNowButton, { force: true });
            await this.page.waitForSelector(this.closePublishFlowButton, { state: 'visible' });
        });
    }

    async clickOnClosePublishFlow() {
        await this.executeWithScreenshot('click_on_close_publish_flow', async () => {
            await this.page.click(this.closePublishFlowButton);
            await this.page.waitForSelector(this.postsListItems, { state: 'visible', timeout: 10000 });
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

    async getPublishedPostsTitles() {
        return await this.executeWithScreenshot('get_published_posts_titles', async () => {
            await this.page.waitForSelector(this.postsListItems, { state: 'visible' });
            const titles = await this.page.$$eval(this.postsListItems, elements =>
                elements.map(el => el.textContent.trim())
            );
            return titles;
        });
    }

    async setPostFeatureImage(imagePath) {
        await this.executeWithScreenshot('set_post_feature_image', async () => {
            await this.page.click(this.featureImageButton);
            const imageInput = await this.page.locator(this.featureImageInput).last();
            await imageInput.setInputFiles(imagePath);
            await this.page.waitForSelector(this.featureImageSelector, { state: 'visible', timeout: 10000 });
        });
    }

    async getPostFeatureImageSrc() {
        return await this.executeWithScreenshot('get_post_feature_image_src', async () => {
            const src = await this.page.getAttribute(this.featureImageSelector, 'src');
            return src; 
        });
    }

    async getPostFeatureEditImageSrc() {
        return await this.executeWithScreenshot('get_post_feature_edit_image_src', async () => {
            const imgEl = await this.page.$(this.featureImageSelector);
            if (!imgEl) return false;
            const src = await imgEl.getAttribute('src');
            return (src && src !== '') ? src : false;
        });
    }

    async clickOnSchedulePost() {
        await this.executeWithScreenshot('click_on_schedule_post', async () => {
            await this.page.click(this.scheduleSettingButton);
            await this.page.waitForSelector(this.scheduleForLaterLabel, { state: 'visible' });
            await this.page.click(this.scheduleForLaterLabel, { force: true });
        });
    }

    async getPostStatusByTitle(title) {
        return await this.executeWithScreenshot('get_post_status_by_title', async () => {
            const postElement = this.page.locator(this.postSelectorByTitle(title)).first();
            await expect(postElement).toBeVisible({ timeout: 5000 });

            const statusElement = postElement.locator(this.postStatusSelector).first();
            await expect(statusElement).toBeVisible({ timeout: 5000 });

            const statusText = await statusElement.textContent();
            return statusText?.trim();
        });
    }

    async clickOnPostSettings() {
        await this.executeWithScreenshot('click_on_post_settings', async () => {
            await this.page.waitForSelector(this.settingsMenuButton, { state: 'visible' });
            const isOpen = await this.page.locator(this.tagInputGeneric).isVisible().catch(() => false);
            if (!isOpen) {
                await this.page.click(this.settingsMenuButton);
                await this.page.waitForSelector(this.tagInputGeneric, { state: 'visible', timeout: 10000 });
            }
        });
    }

    async assignTagToPost(tagName) {
        await this.executeWithScreenshot('assign_tag_to_post', async () => {
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

    async clickOnGoBackToPosts() {
        await this.executeWithScreenshot('click_on_go_back_to_posts', async () => {
            await this.page.click(this.goBackToPostsButton);
            await this.page.waitForSelector(this.postsListItems, { state: 'visible' });
        });
    }

    async getPostTags() {
        return await this.executeWithScreenshot('get_post_tags', async () => {
            const tags = await this.page.$$eval(this.assignedTagsList, elements =>
                elements.map(el => el.textContent.trim())
            );
            return tags.join(', ');
        });
    }

    async setNewPostTitle(title) {
        await this.executeWithScreenshot('set_new_post_title', async () => {
            await this.page.fill(this.titleInput, '');
            await this.page.fill(this.titleInput, title);
        });
    }


    async clickOnUpdate() {
        await this.executeWithScreenshot('click_on_update', async () => {
            const btn = this.page.locator(this.updateButton).first();
            await btn.click();
            await this.page.waitForLoadState('networkidle');
        });
    }

    async clickOnPosts() {
        await this.executeWithScreenshot('click_on_posts', async () => {
            await this.page.click(this.postsButton);
        });
    }

    async getPostRowByTitle(title) {
        return await this.executeWithScreenshot('get_post_row_by_title', async () => {
            const row = this.page.locator(this.postsListItems, { hasText: title }); 
            await row.first().waitFor({ state: 'visible' });
            return row.first();
        });
    }

    async deleteFeatureImage() {
        await this.executeWithScreenshot('delete_feature_image', async () => {
            const imageSrcOrFalse = await this.getPostFeatureEditImageSrc();

            if (!imageSrcOrFalse) {
                console.log('No hay imagen para eliminar.');
                return false;
            }

            const imageOverlay = this.page.locator(this.imagePost);
            await imageOverlay.hover();
            
            await this.page.waitForSelector(this.deleteButton, { state: 'visible' });
            await this.page.click(this.deleteButton, { force: true });
            
            await this.page.waitForSelector(this.imageLocator, { state: 'detached', timeout: 5000 });

            const stillThere = await this.page.locator(this.imageLocator).count();
            
            if (stillThere === 0) {
                return true;
            } else {
                console.log('La imagen aún está presente.');
                return false;
            }
        });
    }

    async clickOnSettingsSideBar() {
        await this.executeWithScreenshot('click_on_settings_side_bar', async () => {
            await this.page.click(this.settingsMenuButton);
            await this.page.waitForSelector(this.postHistoryButton, { state: 'visible' });
        });
    }

    async clickOnPostHistory() {
        await this.executeWithScreenshot('click_on_post_history', async () => {        
            await this.page.click(this.postHistoryButton);
            await this.page.waitForSelector(this.publishedVersionSelector, { state: 'visible' });
        });
    }

    async clickOnPublishedVersion() {
        await this.executeWithScreenshot('click_on_published_version', async () => {
            const btn = this.page.locator(this.publishedVersionSelector);
            const visible = await btn.isVisible().catch(() => false);
            
            if (!visible) return false;

            await btn.click();
            await this.page.waitForSelector(this.restoreButton, { state: 'visible' });
            return true;
        });
    }

    async clickOnRestoreVersion() {
        await this.executeWithScreenshot('click_on_restore_version', async () => {
            const btn = this.page.locator(this.restoreButton);
            const visible = await btn.isVisible().catch(() => false);
            
            if (!visible) return false;

            await btn.click({ trial: false });
            await this.page.waitForSelector(this.restoreBanner, { state: 'visible' });
            return true;
        });
    }

    async clickOnRestorePost() {
        await this.executeWithScreenshot('click_on_restore_post', async () => {
            const modal = this.page.locator(this.restoreBanner);
            const appeared = await modal.waitFor({ state: 'visible', timeout: 5000 }).then(() => true).catch(() => false);

            if (!appeared) return false;
            
            const confirmBtn = modal.locator(this.restorePostButton);
            await confirmBtn.click();
            
            await modal.waitFor({ state: 'detached', timeout: 5000 }).catch(() => {});
            return true;
        });
    }

    async getEditorPostTitle() {
        return await this.executeWithScreenshot('get_editor_post_title', async () => {
            const locator = this.page.locator(this.titleConfirmation).first();
            const exists = await locator.count();

            if (exists === 0) {
                return false;
            }
            
            await locator.waitFor({ state: 'visible' });
            const text = await locator.innerText();
            return text.trim();
        });
    }

    async clickOnPostByTitle(titleToFind) { 
        await this.executeWithScreenshot('click_on_post_by_title', async () => {
            await this.page.waitForSelector(this.postsListItems, { state: 'visible', timeout: 10000 });
            
            const titleLocator = this.page.locator(this.postsListItems, { hasText: titleToFind }); 
            
            const count = await titleLocator.count(); 
            if (count === 0) { 
                console.log(`Post with the title: ${titleToFind}, has not been found`); 
                return false; 
            }

            const liLocator = titleLocator.first().locator('..'); 
            const listItem = liLocator.locator('..'); 
            
            await listItem.click(); 
            await this.page.waitForSelector(this.titleInput, { state: 'visible', timeout: 10000 });
            
            return true; 
        });
    }

    async deletePost() {
        await this.executeWithScreenshot('delete_post', async () => {
            await this.page.click(this.postDeleteButton);
            await this.page.waitForSelector(this.deleteBanner, { state: 'visible' });
        });
    }

    async deleteConfirmation() {
        await this.executeWithScreenshot('delete_confirmation', async () => {
            const modal = this.page.locator(this.deleteBanner);
            const appeared = await modal.waitFor({ state: 'visible', timeout: 5000 }).then(() => true).catch(() => false);

            if (!appeared) return false;

            const confirmBtn = modal.locator(this.deletePostButton);
            await confirmBtn.click();
            
            await modal.waitFor({ state: 'detached', timeout: 5000 }).catch(() => {});
            await this.page.waitForSelector(this.postsListItems, { state: 'visible' });
            
            return true;
        });
    }
}