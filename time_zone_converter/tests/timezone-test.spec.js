const { test, expect } = require('@playwright/test');
const fs = require('fs');

// Create screenshots directory if it doesn't exist
const screenshotDir = './screenshots';
if (!fs.existsSync(screenshotDir)) {
    fs.mkdirSync(screenshotDir);
}

test('Timezone Converter Full UI Workflow', async ({ page }) => {
    // 1. Navigate to the page
    await page.goto('http://localhost:8000/timezone_converter.html');
    
    // 2. Initial Screenshot
    await page.screenshot({ path: `${screenshotDir}/1-base-page.png` });

    // 3. Test the slider (540 = 9:00 AM)
    const slider = page.locator('#timeSlider');
    await slider.fill('540');
    // Dispatch 'input' event to ensure the JS 'oninput' handler triggers
    await slider.dispatchEvent('input');
    
    // 4. Verify the time display shows "09:00"
    const timeInput = page.locator('#timeInput');
    await expect(timeInput).toHaveValue('09:00');
    await page.screenshot({ path: `${screenshotDir}/2-slider-set-9am.png` });

    // 5. Test direct time input by typing "14:30"
    await timeInput.fill('14:30');
    await timeInput.press('Enter');
    
    // Verify results updated (check for a specific converted time if known)
    await expect(timeInput).toHaveValue('14:30');
    await page.screenshot({ path: `${screenshotDir}/3-direct-input-entry.png` });

    // 6. Change anchor timezone and verify conversions
    const anchorSelect = page.locator('#anchorTimezone');
    await anchorSelect.selectOption('India');
    
    // Confirm the conversion grid updated (checking visibility of a time box)
    const grid = page.locator('#conversionTimeGrid');
    await expect(grid).toBeVisible();
    
    // We check if "India" box now matches our input "14:30"
    const indiaBox = grid.locator('.time-box', { hasText: 'India' }).locator('.time-display');
    await expect(indiaBox).toHaveText('14:30');
    
    await page.screenshot({ path: `${screenshotDir}/4-timezone-changed-to-india.png` });
});

