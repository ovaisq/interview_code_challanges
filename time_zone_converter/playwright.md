### Howto

```bash
> npm install
> npm install -D @playwright/test
> npx playwright install chromium
> npm run serve
> npx playwright test math-validation.spec.js
> npx playwright test timezone-test.spec.js --headed
```
```shell
> npx playwright test tests/functional-tests.spec.js

Running 18 tests using 5 workers

  ✓   1 …l-tests.spec.js:40:13 › Timezone Converter Functional Suite › Anchor: India › should verify manual time input updates the grid for India (1.4s)
  ✓   2 …sts.spec.js:59:13 › Timezone Converter Functional Suite › Anchor: Pacific › should verify slider updates both input and grid for Pacific (1.3s)
  ✓   3 …ne Converter Functional Suite › Anchor: Pacific › should verify changing anchor keeps slider position but recalculates times for Pacific (1.9s)
  ✓   4 …sts.spec.js:40:13 › Timezone Converter Functional Suite › Anchor: Pacific › should verify manual time input updates the grid for Pacific (1.3s)
  ✓   5 …l-tests.spec.js:59:13 › Timezone Converter Functional Suite › Anchor: India › should verify slider updates both input and grid for India (1.3s)
  ✓   6 …mezone Converter Functional Suite › Anchor: India › should verify changing anchor keeps slider position but recalculates times for India (1.8s)
  ✓   7 …sts.spec.js:40:13 › Timezone Converter Functional Suite › Anchor: Central › should verify manual time input updates the grid for Central (1.2s)
  ✓   8 …sts.spec.js:59:13 › Timezone Converter Functional Suite › Anchor: Central › should verify slider updates both input and grid for Central (1.2s)
  ✓   9 …ne Converter Functional Suite › Anchor: Central › should verify changing anchor keeps slider position but recalculates times for Central (1.7s)
  ✓  10 …sts.spec.js:40:13 › Timezone Converter Functional Suite › Anchor: Eastern › should verify manual time input updates the grid for Eastern (1.2s)
  ✓  11 …sts.spec.js:59:13 › Timezone Converter Functional Suite › Anchor: Eastern › should verify slider updates both input and grid for Eastern (1.2s)
  ✓  12 …ne Converter Functional Suite › Anchor: Eastern › should verify changing anchor keeps slider position but recalculates times for Eastern (1.7s)
  ✓  13 …um] › tests/functional-tests.spec.js:124:5 › Timezone Converter Functional Suite › should verify all four timezones are always displayed (1.2s)
  ✓  14 …hromium] › tests/functional-tests.spec.js:138:5 › Timezone Converter Functional Suite › should verify slider and input stay synchronized (2.2s)
  ✓  15 …sts/functional-tests.spec.js:162:5 › Timezone Converter Functional Suite › should validate invalid time inputs are rejected or corrected (1.9s)
  ✓  16 [chromium] › tests/functional-tests.spec.js:186:5 › Timezone Converter Functional Suite › should handle edge case times correctly (2.2s)
  ✓  17 …um] › tests/functional-tests.spec.js:210:5 › Timezone Converter Functional Suite › should verify anchor dropdown reflects current anchor (4.0s)
  ✓  18 …tests.spec.js:230:5 › Timezone Converter Functional Suite › should verify conversions update when anchor changes at same slider position (2.3s)

  18 passed (9.0s)

To open last HTML report run:

  npx playwright show-report
```
