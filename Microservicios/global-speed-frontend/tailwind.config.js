/** @type {import('tailwindcss').Config} */
module.exports = {
    content: [
      "./src/**/*.{js,ts,jsx,tsx}",
      "./src/components/ui/Button.tsx",
      "./src/components/ui/Input.tsx",
      "./src/pages/_app.tsx",
      "./src/pages/login.tsx",
      "./src/modules/auth/LoginForm.tsx",
      "./src/services/authService.tsx",
      "./src/store/authSlice.ts",
      "./src/styles/globals.css",
    ],
    theme: {
      extend: {},
    },
    plugins: [],
  };
  