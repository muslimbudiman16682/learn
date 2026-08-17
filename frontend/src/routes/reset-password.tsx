import { zodResolver } from "@hookform/resolvers/zod"
import { useMutation } from "@tanstack/react-query"
import {
  createFileRoute,
  Link as RouterLink,
  redirect,
  useNavigate,
} from "@tanstack/react-router"
import type { TFunction } from "i18next"
import { useForm } from "react-hook-form"
import { useTranslation } from "react-i18next"
import { z } from "zod"

import { LoginService } from "@/client"
import { AuthLayout } from "@/components/Common/AuthLayout"
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form"
import { LoadingButton } from "@/components/ui/loading-button"
import { PasswordInput } from "@/components/ui/password-input"
import { isLoggedIn } from "@/hooks/useAuth"
import useCustomToast from "@/hooks/useCustomToast"
import { handleError } from "@/utils"

const searchSchema = z.object({
  token: z.string().catch(""),
})

const buildFormSchema = (t: TFunction) =>
  z
    .object({
      new_password: z
        .string()
        .min(1, { message: t("validation.passwordRequired") })
        .min(8, { message: t("validation.passwordMin") }),
      confirm_password: z
        .string()
        .min(1, { message: t("validation.confirmPasswordRequired") }),
    })
    .refine((data) => data.new_password === data.confirm_password, {
      message: t("validation.passwordsDontMatch"),
      path: ["confirm_password"],
    })

type FormData = z.infer<ReturnType<typeof buildFormSchema>>

export const Route = createFileRoute("/reset-password")({
  component: ResetPassword,
  validateSearch: searchSchema,
  beforeLoad: async ({ search }) => {
    if (isLoggedIn()) {
      throw redirect({ to: "/" })
    }
    if (!search.token) {
      throw redirect({ to: "/login" })
    }
  },
  head: () => ({
    meta: [
      {
        title: "Reset Password - FastAPI Template",
      },
    ],
  }),
})

function ResetPassword() {
  const { t } = useTranslation()
  const { token } = Route.useSearch()
  const { showSuccessToast, showErrorToast } = useCustomToast()
  const navigate = useNavigate()
  const formSchema = buildFormSchema(t)

  const form = useForm<FormData>({
    resolver: zodResolver(formSchema),
    mode: "onBlur",
    criteriaMode: "all",
    defaultValues: {
      new_password: "",
      confirm_password: "",
    },
  })

  const mutation = useMutation({
    mutationFn: (data: { new_password: string; token: string }) =>
      LoginService.resetPassword({ body: data }),
    onSuccess: () => {
      showSuccessToast(t("auth.resetPassword.successToast"))
      form.reset()
      navigate({ to: "/login" })
    },
    onError: handleError.bind(showErrorToast),
  })

  const onSubmit = (data: FormData) => {
    mutation.mutate({ new_password: data.new_password, token })
  }

  return (
    <AuthLayout>
      <Form {...form}>
        <form
          onSubmit={form.handleSubmit(onSubmit)}
          className="flex flex-col gap-6"
        >
          <div className="flex flex-col items-center gap-2 text-center">
            <h1 className="text-2xl font-bold">
              {t("auth.resetPassword.title")}
            </h1>
          </div>

          <div className="grid gap-4">
            <FormField
              control={form.control}
              name="new_password"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>{t("auth.resetPassword.newPassword")}</FormLabel>
                  <FormControl>
                    <PasswordInput
                      data-testid="new-password-input"
                      placeholder="New Password"
                      {...field}
                    />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />

            <FormField
              control={form.control}
              name="confirm_password"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>
                    {t("auth.resetPassword.confirmPassword")}
                  </FormLabel>
                  <FormControl>
                    <PasswordInput
                      data-testid="confirm-password-input"
                      placeholder="Confirm Password"
                      {...field}
                    />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />

            <LoadingButton
              type="submit"
              className="w-full"
              loading={mutation.isPending}
            >
              {t("auth.resetPassword.submit")}
            </LoadingButton>
          </div>

          <div className="text-center text-sm">
            {t("auth.resetPassword.rememberPassword")}{" "}
            <RouterLink to="/login" className="underline underline-offset-4">
              {t("auth.resetPassword.logIn")}
            </RouterLink>
          </div>
        </form>
      </Form>
    </AuthLayout>
  )
}
