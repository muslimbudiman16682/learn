import { useSuspenseQuery } from "@tanstack/react-query"
import { createFileRoute, redirect } from "@tanstack/react-router"
import { ShieldCheck } from "lucide-react"
import { Suspense, useMemo } from "react"
import { useTranslation } from "react-i18next"

import { PermissionsService, UsersService } from "@/client"
import { DataTable } from "@/components/Common/DataTable"
import PendingPermissions from "@/components/Pending/PendingPermissions"
import AddPermission from "@/components/Permissions/AddPermission"
import { getColumns } from "@/components/Permissions/columns"

function getPermissionsQueryOptions() {
  return {
    queryFn: async () =>
      (
        await PermissionsService.readPermissions({
          query: { skip: 0, limit: 100 },
        })
      ).data,
    queryKey: ["permissions"],
  }
}

export const Route = createFileRoute("/_layout/permissions")({
  component: Permissions,
  beforeLoad: async () => {
    const { data: user } = await UsersService.readUserMe()
    if (!user.is_superuser) {
      throw redirect({
        to: "/",
      })
    }
  },
  head: () => ({
    meta: [
      {
        title: "Permissions - FastAPI Template",
      },
    ],
  }),
})

function PermissionsTableContent() {
  const { t } = useTranslation()
  const { data: permissions } = useSuspenseQuery(getPermissionsQueryOptions())
  const columns = useMemo(() => getColumns(t), [t])

  if (permissions.data.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center text-center py-12">
        <div className="rounded-full bg-muted p-4 mb-4">
          <ShieldCheck className="h-8 w-8 text-muted-foreground" />
        </div>
        <h3 className="text-lg font-semibold">
          {t("permissions.empty.title")}
        </h3>
        <p className="text-muted-foreground">
          {t("permissions.empty.subtitle")}
        </p>
      </div>
    )
  }

  return <DataTable columns={columns} data={permissions.data} />
}

function PermissionsTable() {
  return (
    <Suspense fallback={<PendingPermissions />}>
      <PermissionsTableContent />
    </Suspense>
  )
}

function Permissions() {
  const { t } = useTranslation()

  return (
    <div className="flex flex-col gap-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold tracking-tight">
            {t("permissions.title")}
          </h1>
          <p className="text-muted-foreground">{t("permissions.subtitle")}</p>
        </div>
        <AddPermission />
      </div>
      <PermissionsTable />
    </div>
  )
}
