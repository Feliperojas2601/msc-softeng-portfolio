import { BasePage } from './base-page.js';

export class PostPage extends BasePage {
    constructor(page, screenshotManager = null) {
        super(page, screenshotManager);
        this.newPostButton = 'a[href="#/editor/post/"]';
        this.titleInput = 'textarea.gh-editor-title';
        this.contentInput = 'div.koenig-editor__editor';
        this.contentParagraph = 'div.koenig-editor__editor p';
        this.publishButton = 'div.gh-publishmenu-trigger';
        this.setItLiveNowOption = 'div.gh-publishmenu-radio.active';
        this.scheduleForLaterOption = 'div.gh-publishmenu-radio:not(.active)';
        this.continueButton = 'button.gh-publishmenu-button';
        this.publishModal = '.publish-modal';
        this.rightNowButton = 'button[data-test-button="confirm-publish"]';
        this.closePublishFlowButton = 'a[href="#/posts/"]';
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
        this.settingsMenuButton = 'button.gh-actions-cog';
        this.closeSettingsButton = 'button.close.settings-menu-header-action';
        this.leaveButton = 'button.gh-btn-red:has-text("Leave")';
        this.tagInput = 'input#ember-power-select-trigger-multiple-input-ember427';
        this.tagInputGeneric = 'input.ember-power-select-trigger-multiple-input';
        this.goBackToPostsButton = 'a[href="#/posts/"]';
        this.assignedTagsList = 'li.ember-power-select-multiple-option';
        this.bodyContentInput = 'div[class="kg-prose"]';
        this.firstPost = 'a[class="ember-view permalink gh-list-data gh-post-list-title"]';
        this.updateButton = 'div.gh-publishmenu-trigger';
        this.updateConfirmButton = 'button.gh-publishmenu-button';
        this.postsButton = 'a[href="#/posts/"]';
        this.imagePost = 'div[class="gh-editor-feature-image-overlay"]';
        this.deleteButton = 'button[class="image-action image-delete"]';
        this.postHistoryButton = 'button[data-test-toggle="post-history"]';
        this.publishedVersionSelector = 'button[data-test-button="preview-revision"]';
        this.restoreButton = 'button[class="gh-post-history-version-restore"]';
        this.restorePostButton = 'button[data-test-button="restore"]';
        this.restoreBanner = 'div[data-test-modal="restore-revision"]';
        this.titleConfirmation = 'div[class="gh-editor-title"]';
        this.postDeleteButton = '.settings-menu-pane button.settings-menu-delete-button';
        this.pageLocator = 'li.gh-list-row.gh-posts-list-item';
        this.imageLocator = 'div.gh-editor-feature-image img';
        this.deleteBanner = 'div.modal-footer';
        this.deletePostButtonConfirmation = 'button.gh-btn-red:has-text("Delete")';
    }

    async clickOnNewPost() {
        await this.executeWithScreenshot('click_on_new_post', async () => {
            await this.page.click(this.newPostButton);
            await this.page.waitForTimeout(3000);
        });
    }

    async setPostTitle(title) {
        await this.executeWithScreenshot('set_post_title', async () => {
            await this.page.click(this.titleInput);
            await this.page.fill(this.titleInput, title);
            await this.page.waitForTimeout(1000);
        });
    }

    async setPostContent(content) {
        await this.executeWithScreenshot('set_post_content', async () => {
            await this.page.click(this.contentInput);
            await this.page.waitForTimeout(1000);
            await this.page.keyboard.type(content);
            await this.page.waitForTimeout(1000);
        });
    }

    async clickOnPublishPost() {
        await this.executeWithScreenshot('click_on_publish_post', async () => {
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

    async clickOnRightNowPublishPost() {
        await this.executeWithScreenshot('click_on_right_now_publish_post', async () => {
            await this.page.waitForTimeout(1000);
        });
    }

    async clickOnClosePublishFlow() {
        await this.executeWithScreenshot('click_on_close_publish_flow', async () => {
            await this.page.click(this.closePublishFlowButton);
            await this.page.waitForTimeout(1000);
        });
    }

    async getPublishedPostsTitles() {
        return await this.executeWithScreenshot('get_published_posts_titles', async () => {
            const titles = await this.page.$$eval(this.postsListItems, elements =>
                elements.map(el => el.textContent.trim())
            );
            return titles;
        });
    }

    async setPostFeatureImage() {
        await this.executeWithScreenshot('set_post_feature_image', async () => {
            await this.page.waitForTimeout(1000);
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
            await this.page.waitForTimeout(2000);
            await this.page.click(this.scheduleForLaterLabel, { force: true });
            await this.page.waitForTimeout(2000);
        });
    }

    async getPostStatusByTitle(title) {
        return await this.executeWithScreenshot('get_post_status_by_title', async () => {
            const selector = this.postSelectorByTitle(title);
            await this.page.waitForSelector(selector, { state: 'visible', timeout: 5000 });
            const postElement = this.page.locator(selector);
            const statusElement = postElement.locator(this.postStatusSelector);
            const statusText = await statusElement.textContent();
            return statusText.trim();
        });
    }

    async clickOnPostSettings(goBack = false) {
        await this.executeWithScreenshot('click_on_post_settings', async () => {
            if (goBack) {
                await this.page.click(this.closeSettingsButton);
            } else {
                await this.page.click(this.settingsMenuButton);
            }
            await this.page.waitForTimeout(2000);
        });
    }

    async assignTagToPost(tagName) {
        await this.executeWithScreenshot('assign_tag_to_post', async () => {
            await this.page.waitForTimeout(4000);
            await this.page.click(this.tagInputGeneric);
            await this.page.waitForTimeout(3000);
            await this.page.keyboard.type(tagName);
            await this.page.waitForTimeout(3000);
            await this.page.keyboard.press('Enter');
            await this.page.waitForTimeout(3000);
        });
    }

    async clickOnGoBackToPosts(forceLeave = false) {
        await this.executeWithScreenshot('click_on_go_back_to_posts', async () => {
            await this.page.click(this.goBackToPostsButton);
            if (forceLeave) {
                await this.page.waitForTimeout(2000);
                await this.page.click(this.leaveButton);
            }
            await this.page.waitForTimeout(2000);
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
            await this.page.click(this.titleInput);
            await this.page.fill(this.titleInput, '');
            await this.page.fill(this.titleInput, title);
            await this.page.waitForTimeout(2000);
        });
    }

    async clickOnUpdate() {
        await this.executeWithScreenshot('click_on_update', async () => {
            await this.page.click(this.updateButton);
            await this.page.waitForTimeout(2000);
            await this.page.click(this.updateConfirmButton);
            await this.page.waitForTimeout(2000);
        });
    }

    async clickOnPosts() {
        await this.executeWithScreenshot('click_on_posts', async () => {
            await this.page.click(this.postsButton);
            await this.page.waitForTimeout(2000);
        });
    }

    async getPostRowByTitle(title) {
        return await this.executeWithScreenshot('get_post_row_by_title', async () => {
            const row = this.page.locator(this.pageLocator).filter({ has: this.page.locator(`h3.gh-content-entry-title:text-is("${title}")`) });
            return row.first();
        });
    }

    async deleteFeatureImage() {
        await this.executeWithScreenshot('delete_feature_image', async () => {
            // Confirming existence of image
            const imageSrcOrFalse = await this.getPostFeatureEditImageSrc();

            // Returning false in case it is not present
            if (!imageSrcOrFalse) {
                console.log('No hay imagen para eliminar.');
                return false;
            }

            // Image hover to show delete button
            const imageOverlay = this.page.locator(this.imagePost);

            // Image hover
            await imageOverlay.hover();

            // Max time wait defined
            await this.page.waitForTimeout(200);

            // Clicking in the delete button
            await this.page.click(this.deleteButton, { force: true });
            
            // Waiting for the deletion to process
            await this.page.waitForTimeout(1000);

            // Verifying tag is not present
            const stillThere = await this.page.locator(this.imageLocator).count();
            
            // Returning true if deletion was successful
            if (stillThere === 0) {
                return true;
            } 
            
            // Returning false if deletion was not successful
            else {
                console.log('La imagen aún está presente.');
                return false;
            }
        });
    }

    async clickOnSettingsSideBar() {
        await this.executeWithScreenshot('click_on_settings_side_bar', async () => {
            await this.page.waitForTimeout(2000);
            await this.page.click(this.settingsMenuButton);
            await this.page.waitForTimeout(2000);
        });
    }

    async clickOnPostHistory() {
        await this.executeWithScreenshot('click_on_post_history', async () => {
            await this.page.waitForTimeout(2000);
            await this.page.click(this.postHistoryButton);
            await this.page.waitForTimeout(2000);
        });
    }

    async clickOnPublishedVersion() {
        await this.executeWithScreenshot('click_on_published_version', async () => {
            // Button locating
            const btn = this.page.locator(this.publishedVersionSelector);

            // Confirmando visibilidad
            const visible = await btn.isVisible().catch(() => false);
            
            // Returning false if it is not visible
            if (!visible) return false;

            // Clicking on the button
            await btn.click();

            //
            await this.page.waitForTimeout(200);
            return true;
        });
    }

    async clickOnRestoreVersion() {
        await this.executeWithScreenshot('click_on_restore_version', async () => {
            // Button locating
            const btn = this.page.locator(this.restoreButton);
            
            // Confirming visibility
            const visible = await btn.isVisible().catch(() => false);
            
            // Returning false if it is not visible
            if (!visible) return false;

            // Clicking on the button
            await btn.click({ trial: false });

            // Short wait after clicking
            await this.page.waitForTimeout(1000);

            // Returning true as process completed
            return true;
        });
    }

    async clickOnRestorePost() {
        await this.executeWithScreenshot('click_on_restore_post', async () => {
            // Locating modal
            const modal = this.page.locator(this.restoreBanner);

            // Confirming if banner message appeared
            const appeared = await modal.waitFor({ state: 'visible', timeout: 2500 }).then(() => true).catch(() => false);

            // Returning false if not appeared
            if (!appeared) return false;

            // Clicking on confirm button
            const confirmBtn = modal.locator(this.restorePostButton);
            await confirmBtn.click();
            
            // Waiting for modal to disappear
            await modal.waitFor({ state: 'detached', timeout: 2500 }).catch(() => {});
            
            // Short wait after modal close
            await this.page.waitForTimeout(1000);
            
            // Returning true as process completed
            return true;
        });
    }

    async getEditorPostTitle() {
        return await this.executeWithScreenshot('get_editor_post_title', async () => {
            // Locating title element
            const locator = this.page.locator(this.titleConfirmation).first();
            
            // Checking if element exists
            const exists = await locator.count();

            // Returning false if not exists
            if (exists === 0) {
                return false;
            }
            
            // Getting and returning trimmed text
            const text = await locator.innerText();
            return text.trim();
        });
    }

    async clickOnPostByTitle(titleToFind) { 
        await this.executeWithScreenshot('click_on_post_by_title', async () => {
            
            // Short wait after clicking 
            await this.page.waitForTimeout(2500); 
            
            // Locating the h3 tag with the expected value 
            const titleLocator = this.page.locator(this.postsListItems, { hasText: titleToFind }); 
            
            // Confirm if there is at least one match 
            const count = await titleLocator.count(); 
            if (count === 0) { 
                console.log(`Post with the title: ${titleToFind}, has not been found`); 
                return false; 
            }
            // Takes the first match, goes to its parent <a> and then to the <li> 
            const liLocator = titleLocator.first().locator('..'); 
            
            // Goes one level up to the <li> 
            const listItem = liLocator.locator('..'); 
            
            // Click on <li> 
            await listItem.click(); 
            
            // Short wait after clicking 
            await this.page.waitForTimeout(4000); 
            
            
            // Retruning true as process completed
            return true; 
        });
    }

    async deletePost() {
        await this.executeWithScreenshot('delete_post', async () => {
            await this.page.waitForTimeout(4000);
            await this.page.click(this.postDeleteButton);
            await this.page.waitForTimeout(2000);
        });
    }

    async deleteConfirmation() {
        await this.executeWithScreenshot('delete_confirmation', async () => {
            await this.page.waitForTimeout(4000);
            await this.page.click(this.deletePostButtonConfirmation);
            await this.page.waitForTimeout(2000);
            return true;
        });
    }
}