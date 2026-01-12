const { test, expect } = require('@playwright/test');

test.describe('Timezone Converter Functional Suite', () => {
    // List of anchors to test against
    const anchors = ['Pacific', 'India', 'Central', 'Eastern'];
    
    test.beforeEach(async ({ page }) => {
        await page.goto('http://localhost:8000/timezone_converter.html');
        await page.waitForLoadState('networkidle');
    });
    
    /**
     * Helper to get conversion time from grid using page.evaluate()
     * More reliable than complex locator chains
     */
    async function getGridTime(page, zoneName) {
        await page.waitForSelector('#conversionTimeGrid .time-box', { timeout: 5000 });
        
        const timeString = await page.evaluate((zone) => {
            const timeBoxes = document.querySelectorAll('#conversionTimeGrid .time-box');
            for (const box of timeBoxes) {
                const label = box.querySelector('label');
                if (label && label.textContent.trim() === zone) {
                    const timeDisplay = box.querySelector('.time-display');
                    return timeDisplay ? timeDisplay.textContent.trim() : null;
                }
            }
            return null;
        }, zoneName);
        
        if (!timeString) {
            throw new Error(`Could not find time for zone: ${zoneName}`);
        }
        
        return timeString;
    }
    
    for (const anchor of anchors) {
        test.describe(`Anchor: ${anchor}`, () => {
            test(`should verify manual time input updates the grid for ${anchor}`, async ({ page }) => {
                const testTime = '14:45';
                
                // 1. Set the Anchor via the dropdown
                await page.selectOption('#anchorTimezone', anchor);
                
                // 2. Enter time directly
                const input = page.locator('#timeInput');
                await input.fill(testTime);
                await input.press('Enter');
                
                // 3. Wait for UI to update
                await page.waitForTimeout(500);
                
                // 4. Verify the display box for this anchor matches the input
                const displayedTime = await getGridTime(page, anchor);
                expect(displayedTime).toBe(testTime);
            });
            
            test(`should verify slider updates both input and grid for ${anchor}`, async ({ page }) => {
                // 600 minutes = 10:00 AM
                const sliderVal = '600';
                const expectedTime = '10:00';
                
                // 1. Set the Anchor
                await page.selectOption('#anchorTimezone', anchor);
                
                // 2. Move slider
                const slider = page.locator('#timeSlider');
                await slider.fill(sliderVal);
                
                // 3. Wait for updates to propagate
                await page.waitForTimeout(500);
                
                // 4. Verify input field updated
                await expect(page.locator('#timeInput')).toHaveValue(expectedTime);
                
                // 5. Verify slider value display updated
                await expect(page.locator('#sliderValue')).toHaveText(expectedTime);
                
                // 6. Verify grid display updated
                const displayedTime = await getGridTime(page, anchor);
                expect(displayedTime).toBe(expectedTime);
            });
            
            test(`should verify changing anchor keeps slider position but recalculates times for ${anchor}`, async ({ page }) => {
                const testTime = '12:00';
                
                // 1. Set initial time with current anchor
                await page.selectOption('#anchorTimezone', anchor);
                await page.fill('#timeInput', testTime);
                await page.press('#timeInput', 'Enter');
                await page.waitForTimeout(500);
                
                // 2. Verify anchor timezone shows the input time
                const anchorTime = await getGridTime(page, anchor);
                expect(anchorTime).toBe(testTime);
                
                // 3. Change to a different anchor
                const newAnchor = anchors.find(a => a !== anchor);
                if (newAnchor) {
                    await page.selectOption('#anchorTimezone', newAnchor);
                    await page.waitForTimeout(500);
                    
                    // 4. Verify the INPUT FIELD still shows 12:00
                    // (The slider position/input doesn't change when you change anchors)
                    const inputValue = await page.locator('#timeInput').inputValue();
                    expect(inputValue).toBe(testTime);
                    
                    // 5. Verify the NEW anchor timezone now shows 12:00 in the grid
                    // (Because the slider is still at 12:00, but now it's anchored to the new timezone)
                    const newAnchorGridTime = await getGridTime(page, newAnchor);
                    expect(newAnchorGridTime).toBe(testTime);
                    
                    // 6. Verify the OLD anchor timezone now shows a DIFFERENT time
                    // (Because we're no longer anchored to it, it's now a conversion)
                    const oldAnchorGridTime = await getGridTime(page, anchor);
                    // It should NOT be 12:00 anymore (unless it's the same timezone, which it isn't)
                    expect(oldAnchorGridTime).not.toBe(testTime);
                }
            });
        });
    }
    
    test('should verify all four timezones are always displayed', async ({ page }) => {
        const testTime = '15:30';
        
        await page.fill('#timeInput', testTime);
        await page.press('#timeInput', 'Enter');
        await page.waitForTimeout(500);
        
        // Verify all timezone boxes exist and show valid times
        for (const zone of anchors) {
            const time = await getGridTime(page, zone);
            expect(time).toMatch(/^\d{2}:\d{2}$/);
        }
    });
    
    test('should verify slider and input stay synchronized', async ({ page }) => {
        const testValues = [
            { slider: '0', time: '00:00' },
            { slider: '540', time: '09:00' },
            { slider: '720', time: '12:00' },
            { slider: '1020', time: '17:00' },
            { slider: '1439', time: '23:59' }
        ];
        
        for (const { slider, time } of testValues) {
            // Move slider
            await page.fill('#timeSlider', slider);
            await page.waitForTimeout(300);
            
            // Check input matches
            const inputValue = await page.locator('#timeInput').inputValue();
            expect(inputValue).toBe(time);
            
            // Check slider display matches
            const sliderDisplay = await page.locator('#sliderValue').textContent();
            expect(sliderDisplay).toBe(time);
        }
    });
    
    test('should validate invalid time inputs are rejected or corrected', async ({ page }) => {
        const invalidInputs = [
            '25:00',  // Invalid hour
            '12:70',  // Invalid minute
            'ab:cd',  // Non-numeric
            '99:99'   // Both invalid
        ];
        
        for (const invalidInput of invalidInputs) {
            await page.fill('#timeInput', invalidInput);
            await page.press('#timeInput', 'Enter');
            await page.waitForTimeout(300);
            
            // Input should be corrected or reverted
            const actualValue = await page.locator('#timeInput').inputValue();
            
            // Should be a valid time format
            expect(actualValue).toMatch(/^([0-1][0-9]|2[0-3]):[0-5][0-9]$/);
            
            // Should NOT be the invalid input we entered
            expect(actualValue).not.toBe(invalidInput);
        }
    });
    
    test('should handle edge case times correctly', async ({ page }) => {
        const edgeCases = [
            { input: '00:00', description: 'midnight' },
            { input: '12:00', description: 'noon' },
            { input: '23:59', description: 'end of day' }
        ];
        
        for (const { input, description } of edgeCases) {
            await page.fill('#timeInput', input);
            await page.press('#timeInput', 'Enter');
            await page.waitForTimeout(500);
            
            // Verify input is preserved
            const actualValue = await page.locator('#timeInput').inputValue();
            expect(actualValue).toBe(input);
            
            // Verify all timezones display valid times
            for (const zone of anchors) {
                const time = await getGridTime(page, zone);
                expect(time).toMatch(/^\d{2}:\d{2}$/);
            }
        }
    });
    
    test('should verify anchor dropdown reflects current anchor', async ({ page }) => {
        for (const anchor of anchors) {
            // Select anchor
            await page.selectOption('#anchorTimezone', anchor);
            await page.waitForTimeout(300);
            
            // Verify dropdown shows selected anchor
            const selectedValue = await page.locator('#anchorTimezone').inputValue();
            expect(selectedValue).toBe(anchor);
            
            // Set a time and verify that timezone shows it
            await page.fill('#timeInput', '15:00');
            await page.press('#timeInput', 'Enter');
            await page.waitForTimeout(500);
            
            const gridTime = await getGridTime(page, anchor);
            expect(gridTime).toBe('15:00');
        }
    });
    
    test('should verify conversions update when anchor changes at same slider position', async ({ page }) => {
        const sliderValue = '720'; // 12:00
        
        // Set slider to noon
        await page.fill('#timeSlider', sliderValue);
        await page.waitForTimeout(500);
        
        // Record all times with Pacific as anchor
        await page.selectOption('#anchorTimezone', 'Pacific');
        await page.waitForTimeout(500);
        
        const pacificAnchoredTimes = {};
        for (const zone of anchors) {
            pacificAnchoredTimes[zone] = await getGridTime(page, zone);
        }
        
        // Pacific should show 12:00
        expect(pacificAnchoredTimes['Pacific']).toBe('12:00');
        
        // Change to Eastern anchor (slider still at 720)
        await page.selectOption('#anchorTimezone', 'Eastern');
        await page.waitForTimeout(500);
        
        const easternAnchoredTimes = {};
        for (const zone of anchors) {
            easternAnchoredTimes[zone] = await getGridTime(page, zone);
        }
        
        // Eastern should now show 12:00
        expect(easternAnchoredTimes['Eastern']).toBe('12:00');
        
        // Pacific should now show a different time (9:00 if no DST, or 8:00/10:00 with DST)
        expect(easternAnchoredTimes['Pacific']).not.toBe('12:00');
        expect(easternAnchoredTimes['Pacific']).not.toBe(pacificAnchoredTimes['Pacific']);
        
        // All times should be valid
        for (const zone of anchors) {
            expect(easternAnchoredTimes[zone]).toMatch(/^\d{2}:\d{2}$/);
        }
    });
});
