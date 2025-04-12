import React, { useState } from "react";
import { useForm } from "react-hook-form";
import { login } from "@/services/authService";
import { useAuthStore } from "@/store/authSlice";
import { toast } from "react-toastify";
import Input from "@/components/ui/Input";
import Button from "@/components/ui/Button";

interface LoginFormInputs {
  email: string;
  password: string;
}

const LoginForm: React.FC = () => {
  const { register, handleSubmit, formState: { errors } } = useForm<LoginFormInputs>();
  const { setToken } = useAuthStore();
  const [loading, setLoading] = useState(false);

  const onSubmit = async (data: LoginFormInputs) => {
    setLoading(true);
    try {
      const response = await login(data.email, data.password);
      setToken(response.token);
      toast.success("Inicio de sesión exitoso");
    } catch (error) {
      toast.error(error instanceof Error ? error.message : "Ocurrió un error inesperado");
    }
    setLoading(false);
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="bg-white p-6 rounded-lg shadow-md w-96">
      <h2 className="text-2xl font-bold text-center mb-4">Iniciar Sesión</h2>
      <Input
        label="Correo Electrónico"
        type="email"
        {...register("email", { required: "El email es requerido" })}
        error={errors.email?.message}
      />
      <Input
        label="Contraseña"
        type="password"
        {...register("password", { required: "La contraseña es requerida" })}
        error={errors.password?.message}
      />
      <Button text="Ingresar" isLoading={loading} />
    </form>
  );
};

export default LoginForm;
