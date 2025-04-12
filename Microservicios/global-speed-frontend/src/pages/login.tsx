import React from "react";
import LoginForm from "@/modules/auth/LoginForm";
import { ToastContainer } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";

const LoginPage: React.FC = () => {
  return (
    <div className="flex justify-center items-center h-screen bg-gray-100">
      <ToastContainer />
      <LoginForm />
    </div>
  );
};

export default LoginPage;
