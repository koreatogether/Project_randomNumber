// 기본 ESLint v9+ 설정 예시
export default [
    {
        files: ["*.js"],
        rules: {
            "no-unused-vars": "warn",
            "no-undef": "error",
            "eqeqeq": "warn"
        },
        languageOptions: {
            ecmaVersion: "latest"
        }
    }
];
