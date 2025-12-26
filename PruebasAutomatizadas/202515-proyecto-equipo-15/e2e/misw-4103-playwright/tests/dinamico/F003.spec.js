// Imports
import { test, expect } from "@playwright/test";
import { AuthPage } from "../../pages/auth-page.js";
import { PostPage } from "../../pages/post-page.js";
import { NavbarPage } from "../../pages/navbar-page.js";
import { getRandomTestImagePath } from "../../utils/utils.js";
import { ScreenshotManager } from "../../utils/screenshot-manager.js";
import { getDynamicDataFromMockaroo } from "../../utils/mockaroo-client.js";

// F003: Editar post
test.describe('Create Post Editing Tests', () => {

    // Initialize variables
    let authPage;
    let postPage;
    let navbarPage;
    let newPostTitle;
    let postBodyContent;
    let postHeaderContent;
    let screenshotManager;

    // Defining Schema
    const schema = "d11861a0";

    // Given
    test.beforeEach(async ({ page }, testInfo) => {
        
        // Dynamic data load
        const [record] = await getDynamicDataFromMockaroo(1, schema);
        
        // Mapping fields to testInfo for reporting
        testInfo.dataPool = { 
            id: record.id, 
            post_title: record.post_title, 
            post_content: record.post_content, 
            new_post_title: record.new_post_title };
        
        // Screenshot manager
        screenshotManager = new ScreenshotManager(page, testInfo);
        
        // Preparing pages
        authPage = new AuthPage(page, screenshotManager);
        postPage = new PostPage(page, screenshotManager);
        navbarPage = new NavbarPage(page, screenshotManager);

        // Image paths and post content
        postHeaderContent = testInfo.dataPool.post_title;
        postBodyContent = testInfo.dataPool.post_content;
        newPostTitle = testInfo.dataPool.new_post_title;
        
        // Navigate to page
        await page.goto("", { waitUntil: "domcontentloaded" });
        await page.waitForTimeout(2000);

        // Image path
        let imagePath = getRandomTestImagePath();

        // Page creation per case
        await authPage.loginOrRegister();
        await navbarPage.clickOnPosts();
        await postPage.clickOnNewPost();
        await postPage.setPostTitle(postHeaderContent);
        await postPage.setPostContent(postBodyContent);
        await postPage.setPostFeatureImage(imagePath);
        await postPage.clickOnPublishPost();
        await postPage.clickOnContinueAfterPublish();
        await postPage.clickOnRightNowPublishPost();
        await postPage.clickOnClosePublishFlow();
        await page.waitForTimeout(2000);
    });

    // E008: Editar título de publicación
    test('Editing post header', async ({ page }) => {
        
        // When
        await postPage.clickOnPostByTitle(postHeaderContent);
        await postPage.setNewPostTitle(newPostTitle);
        await page.waitForTimeout(2000);
        await postPage.clickOnUpdate();
        await page.waitForTimeout(2000);
        
        // Then 
        await postPage.clickOnPosts();
        const postRow = await postPage.getPostRowByTitle(newPostTitle);
        await expect(postRow).toBeVisible();
        await screenshotManager.captureFinalStep();
    });

    // E009: Editar imagen principal de publicación
    test('Editing post image', async ({ page }) => {
        
        // Obtaining a new image path
        let imagePath = getRandomTestImagePath()

        // When
        await postPage.clickOnPostByTitle(postHeaderContent);
        const previousImageSrc = await postPage.getPostFeatureEditImageSrc();
        await postPage.deleteFeatureImage();
        await postPage.setPostFeatureImage(imagePath);
        const previousImageSrc2 = await postPage.getPostFeatureEditImageSrc();
        await postPage.clickOnUpdate();
        await page.waitForTimeout(4000);
        await postPage.clickOnPosts();

        // Then
        // Comparing previous image sources
        expect(previousImageSrc2).not.toBe(previousImageSrc);
        await screenshotManager.captureFinalStep();
    });

    // E010: Editar publicación al restaurar una versión previa
    test('Restoring previous post version', async ({ page }) => {
        
        // Obtaining a new image path
        let imagePath = getRandomTestImagePath()

        // When
        await postPage.clickOnPostByTitle(postHeaderContent);
        const title1 = await postPage.getEditorPostTitle();
        const previousImageSrc = await postPage.getPostFeatureEditImageSrc();
        await postPage.deleteFeatureImage();
        await postPage.setPostFeatureImage(imagePath);
        const previousImageSrc2 = await postPage.getPostFeatureEditImageSrc();
        await postPage.clickOnSettingsSideBar();
        await postPage.clickOnPostHistory();
        await postPage.clickOnPublishedVersion();
        await postPage.clickOnRestoreVersion();
        await postPage.clickOnRestorePost();
        const title2 = await postPage.getEditorPostTitle();
        await page.waitForTimeout(2000);

        // Then
        expect(previousImageSrc).not.toBe(previousImageSrc2);
        
        // Comparing previous image sources
        expect(title1).not.toBe(title2);
        await screenshotManager.captureFinalStep();
    });
});