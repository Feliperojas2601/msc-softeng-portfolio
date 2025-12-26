// Imports
import { faker } from "@faker-js/faker";
import { test, expect } from "@playwright/test";
import { AuthPage } from "../../pages/auth-page.js";
import { PostPage } from "../../pages/post-page.js";
import { NavbarPage } from "../../pages/navbar-page.js";
import { getTestImagePath, hashString } from "../../utils/utils.js";
import { ScreenshotManager } from "../../utils/screenshot-manager.js";

// F001: Crear publicación
test.describe('Create Post Tests', () => {
    let authPage;
    let navbarPage;
    let postPage;
    let postTitle;
    let postContent;
    let imagePath;
    let screenshotManager;

    // Given
    test.beforeEach(async ({ page }, testInfo) => {
        const testTitle = testInfo.title;
        const testHash = hashString(testTitle);
        const baseSeed = process.env.FAKER_SEED ? Number.parseInt(process.env.FAKER_SEED) : 42;
        const uniqueSeed = baseSeed + testHash;
        faker.seed(uniqueSeed);
        screenshotManager = new ScreenshotManager(page, testInfo);
        authPage = new AuthPage(page, screenshotManager);
        navbarPage = new NavbarPage(page, screenshotManager);
        postPage = new PostPage(page, screenshotManager);
        postTitle = faker.lorem.sentence();
        postContent = faker.lorem.paragraphs();
        imagePath = getTestImagePath();
        await page.goto("", { waitUntil: "domcontentloaded" });
        await page.waitForTimeout(2000);
    });

    // E001: Crear publicación básica con éxito
    test('Create basic post successfully', async ({ page }) => {
        // When
        await authPage.loginOrRegister();
        await navbarPage.clickOnPosts();
        await postPage.clickOnNewPost();
        await postPage.setPostTitle(postTitle);
        await postPage.setPostContent(postContent);
        await postPage.clickOnPublishPost();
        await postPage.clickOnContinueAfterPublish();
        await postPage.clickOnRightNowPublishPost();
        await postPage.clickOnClosePublishFlow();
        await page.waitForTimeout(2000);

        // Then 
        const publishedPosts = await postPage.getPublishedPostsTitles();
        expect(publishedPosts).toContain(postTitle);
        await screenshotManager.captureFinalStep();
    });

    // E002: Crear publicación con imagen principal con éxito
    test('Create post with feature image successfully', async ({ page }) => {
        // When
        await authPage.loginOrRegister();
        await navbarPage.clickOnPosts();
        await postPage.clickOnNewPost();
        await postPage.setPostTitle(postTitle);
        await postPage.setPostContent(postContent);
        await postPage.setPostFeatureImage(imagePath);
        await postPage.clickOnPublishPost();
        await postPage.clickOnContinueAfterPublish();
        await postPage.clickOnRightNowPublishPost();
        await postPage.clickOnClosePublishFlow();
        await page.waitForTimeout(2000);

        // Then 
        const publishedPosts = await postPage.getPublishedPostsTitles();
        expect(publishedPosts).toContain(postTitle);
        await postPage.clickOnPostByTitle(postTitle);
        const imageSrc = await postPage.getPostFeatureImageSrc();
        expect(imageSrc).toBeTruthy();
        await screenshotManager.captureFinalStep();
    });

    // E003: Crear publicación sin título con éxito
    test('Create basic post without title successfully', async ({ page }) => {
        // When
        await authPage.loginOrRegister();
        await navbarPage.clickOnPosts();
        await postPage.clickOnNewPost();
        await postPage.setPostContent(postContent);
        await postPage.clickOnPublishPost();
        await postPage.clickOnContinueAfterPublish();
        await postPage.clickOnRightNowPublishPost();
        await postPage.clickOnClosePublishFlow();
        await page.waitForTimeout(2000);

        // Then 
        const publishedPosts = await postPage.getPublishedPostsTitles();
        expect(publishedPosts).toContain('(Untitled)');
        await screenshotManager.captureFinalStep();
    });

    // E004: Crear publicación sin contenido con éxito
    test('Create basic post without content successfully', async ({ page }) => {
        // When
        await authPage.loginOrRegister();
        await navbarPage.clickOnPosts();
        await postPage.clickOnNewPost();
        await postPage.setPostTitle(postTitle);
        await postPage.setPostContent('');
        await postPage.clickOnPublishPost();
        await postPage.clickOnContinueAfterPublish();
        await postPage.clickOnRightNowPublishPost();
        await postPage.clickOnClosePublishFlow();
        await page.waitForTimeout(2000);

        // Then
        const publishedPosts = await postPage.getPublishedPostsTitles();
        expect(publishedPosts).toContain(postTitle);
        await screenshotManager.captureFinalStep();
    });

    // E005: Crear publicación y programarla para publicación futura con éxito
    test('Create post and schedule it for future publication successfully', async ({ page }) => {
        // When
        await authPage.loginOrRegister();
        await navbarPage.clickOnPosts();
        await postPage.clickOnNewPost();
        await postPage.setPostTitle(postTitle);
        await postPage.setPostContent(postContent);
        await postPage.clickOnPublishPost();
        await postPage.clickOnSchedulePost();
        await postPage.clickOnContinueAfterPublish();
        await postPage.clickOnRightNowPublishPost();
        await postPage.clickOnClosePublishFlow();
        await page.waitForTimeout(2000);

        // Then
        const publishedPosts = await postPage.getPublishedPostsTitles();
        expect(publishedPosts).toContain(postTitle);
        const postStatus = await postPage.getPostStatusByTitle(postTitle);
        expect(['Scheduled', 'Published']).toContain(postStatus);
        await screenshotManager.captureFinalStep();
    });
});
