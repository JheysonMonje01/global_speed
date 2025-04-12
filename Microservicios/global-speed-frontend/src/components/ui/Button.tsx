import React from "react";

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  text: string;
  isLoading?: boolean;
}

const Button: React.FC<ButtonProps> = ({ text, isLoading, ...rest }) => {
  return (
    <button
      className="w-full bg-blue-600 hover:bg-blue-700 text-white py-2 px-4 rounded-md transition disabled:opacity-50"
      disabled={isLoading}
      {...rest}
    >
      {isLoading ? "Cargando..." : text}
    </button>
  );
};

export default Button;
