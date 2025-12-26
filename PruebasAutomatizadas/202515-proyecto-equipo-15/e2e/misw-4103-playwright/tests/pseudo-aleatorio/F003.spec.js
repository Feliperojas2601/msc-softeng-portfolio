// Imports
import { faker } from "@faker-js/faker";
import { test, expect } from "@playwright/test";
import { AuthPage } from "../../pages/auth-page.js";
import { PostPage } from "../../pages/post-page.js";
import { NavbarPage } from "../../pages/navbar-page.js";
import { ScreenshotManager } from "../../utils/screenshot-manager.js";
import { getRandomTestImagePath, hashString } from "../../utils/utils.js";

// F003: Editar post
test.describe('Create Post Editing Tests', () => {
    
    // Initialize variables
    let authPage;
    let postPage;
    let navbarPage;
    let postBodyContent;
    let postHeaderContent;
    let screenshotManager;

    // Given
    test.beforeEach(async ({ page }, testInfo) => {
        const testTitle = testInfo.title;
        const testHash = hashString(testTitle);
        const baseSeed = process.env.FAKER_SEED ? Number.parseInt(process.env.FAKER_SEED) : 42;
        const uniqueSeed = baseSeed + testHash;
        faker.seed(uniqueSeed);
        screenshotManager = new ScreenshotManager(page, testInfo);
        // Preparing pages
        authPage = new AuthPage(page, screenshotManager);
        postPage = new PostPage(page, screenshotManager);
        navbarPage = new NavbarPage(page, screenshotManager);

        // Image paths and post content
        postHeaderContent = faker.lorem.words(2);
        postBodyContent = faker.lorem.paragraphs();
        
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
        
        // Setting new post title
        let postHeaderNewContent = faker.lorem.words(2);
        
        // When
        await postPage.clickOnPostByTitle(postHeaderContent);
        await postPage.setNewPostTitle(postHeaderNewContent);
        await postPage.clickOnUpdate();
        await page.waitForTimeout(2000);
        
        // Then 
        await postPage.clickOnPosts();
        const postRow = await postPage.getPostRowByTitle(postHeaderNewContent);
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