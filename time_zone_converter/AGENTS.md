# AGENTS.md - Timezone Converter

## Project Overview
This is a timezone converter application with two implementations:
- **Python app**: Gradio-based web app (`time_zone_converter.py`)
- **HTML/JS app**: Standalone single-page app (`timezone_converter.html`)

Tests are written in Playwright (JavaScript).

## Build/Test/Lint Commands

### Python Application
```bash
# Run the Python app
python3 time_zone_converter.py

# Install dependencies
pip3 install -r requirements.txt
```

### HTML/JS Application
```bash
# Serve the HTML app
npm run serve        # python3 -m http.server 8000
npm run serve:win    # python -m http.server 8000 (Windows)
```

### Testing
```bash
# Run all Playwright tests
npx playwright test

# Run specific test file
npx playwright test tests/timezone-test.spec.js
npx playwright test tests/functional-tests.spec.js

# Run specific test
npx playwright test --grep "should verify manual time input"

# Run with UI mode (for debugging)
npx playwright test --ui

# Run tests in headed mode (see browser)
npx playwright test --headed

# Alternative npm scripts (custom test runners)
npm run test           # node twinny-quick-test.js
npm run test:full      # node timezone-converter-tests.js
npm run test:interactive # node twinny-interactive-test.js
```

### Docker
```bash
# Build Docker image
./build_docker.sh

# Or manually:
docker build -t timezone-converter .
docker run -p 7860:7860 timezone-converter
```

## Code Style Guidelines

### Python
- **Python version**: 3.x with type hints
- **Imports**: Standard library first, then third-party (e.g., `gradio`)
- **Naming**: 
  - Functions: `snake_case` (e.g., `format_dt`, `handle_slider_change`)
  - Constants: `UPPERCASE` (e.g., `TIMEZONES`)
  - Variables: `snake_case`
- **Types**: Use type hints (e.g., `def format_dt(dt: datetime, tz_id: str) -> str`)
- **Comments**: Docstrings for functions using `"""Triple quotes"""`
- **Error handling**: Prefer explicit error handling with clear messages
- **Timezone handling**: Use `zoneinfo` (Python 3.9+) or `pytz` for timezone conversions

### JavaScript (Playwright Tests)
- **Style**: Standard JavaScript, ES6+ features
- **Imports**: Use `require()` for CommonJS modules
- **Naming**: 
  - Functions/variables: `camelCase`
  - Test files: `kebab-case.spec.js`
- **Test structure**:
  ```javascript
  test.describe('Feature Suite', () => {
    test.beforeEach(async ({ page }) => { ... });
    
    test('should describe expected behavior', async ({ page }) => {
      // Arrange
      // Act
      // Assert
    });
  });
  ```
- **Locators**: Prefer semantic selectors (`#id`, `.class`) over XPath
- **Waits**: Use Playwright auto-waits; avoid fixed timeouts when possible
- **Screenshots**: Save to `./screenshots/` directory

### HTML/CSS
- **Structure**: Semantic HTML5 elements
- **CSS**: Use CSS custom properties for theming (colors: `#667eea`, `#764ba2`)
- **Responsive**: Mobile-first with `@media` breakpoints
- **Naming**: 
  - IDs: `camelCase` (e.g., `#timeSlider`, `#anchorTimezone`)
  - Classes: `kebab-case` (e.g., `.time-box`, `.time-display`)

## Project Structure
```
time_zone_converter/
├── time_zone_converter.py          # Python Gradio app
├── timezone_converter.html           # Standalone HTML/JS app
├── requirements.txt                  # Python deps (gradio, pytz)
├── package.json                      # Node deps (@playwright/test)
├── playwright.config.js              # Playwright configuration
├── tests/
│   ├── timezone-test.spec.js       # Basic UI workflow tests
│   ├── functional-tests.spec.js      # Comprehensive functional tests
│   └── math-validation.spec.js       # Math validation tests
├── screenshots/                      # Test screenshots
└── test-results/                     # Playwright test outputs
```

## Testing Conventions

### Running Tests Locally
1. Start the server: `npm run serve`
2. In another terminal, run: `npx playwright test`

### Test Coverage
- Slider functionality (time selection)
- Direct time input validation
- Timezone conversion accuracy
- Anchor timezone switching
- Edge cases (midnight, noon, end of day)
- Invalid input handling

### Timezone Configuration
Configured timezones (IANA IDs):
- Pacific: `America/Los_Angeles`
- India: `Asia/Kolkata`
- Central: `US/Central`
- Eastern: `America/New_York`

## CI/CD Notes
- Tests run on Chromium (configure in `playwright.config.js`)
- Screenshots captured on failure
- Videos recorded (`video: 'on'` in config)
- HTML report generated in `playwright-report/`

## Important Implementation Details
- Python app runs on port 7860 (Gradio default)
- HTML app expects server on port 8000 (`baseURL: 'http://localhost:8000'`)
- Slider range: 0-1439 minutes (0:00 to 23:59)
- Time format: 24-hour (`HH:MM`)
