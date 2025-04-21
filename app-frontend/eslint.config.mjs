import { dirname } from "path";
import { fileURLToPath } from "url";
import { FlatCompat } from "@eslint/eslintrc";
import jsdocPlugin from 'eslint-plugin-jsdoc';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const compat = new FlatCompat({
  baseDirectory: __dirname,
});

const eslintConfig = [
  ...compat.extends("next/core-web-vitals", "next/typescript"),
  // Custom rule overrides go here:
  {
    plugins: {
      jsdoc: jsdocPlugin,
    },
    rules: {
      "@next/next/no-html-link-for-pages": "off",
      // JSDoc plugin configuration
      "jsdoc/require-jsdoc": [
        "warn", 
        {
          require: {
            FunctionDeclaration: true,
            MethodDefinition: true,
            ClassDeclaration: true,
            ArrowFunctionExpression: false, // Skip for arrow functions
            FunctionExpression: false, // Skip for function expressions
          },
        },
      ],
      "jsdoc/require-param": "warn",
      "jsdoc/require-returns": "warn",
      "jsdoc/check-alignment": "warn", // Checks JSDoc alignment
      "jsdoc/check-param-names": "warn", // Ensures parameter names are correct
      "jsdoc/check-types": "warn", // Checks if types are properly mentioned in JSDoc
    },
  },
];

export default eslintConfig;
