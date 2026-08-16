import { useSuspenseQuery } from "@tanstack/react-query"
import { createFileRoute, redirect } from "@tanstack/react-router"
import { ShieldCheck } from "lucide-react"
import { Suspense } from "react"

import { PermissionsService, UsersService } from "@/client"
import { DataTable } from "@/components/Common/DataTable"
import PendingPermissions from "@/components/Pending/PendingPermissions"
import AddPermission from "@/components/Permissions/AddPermission"
import { columns } from "@/components/Permissions/columns"

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
  const { data: permissions } = useSuspenseQuery(getPermissionsQueryOptions())

  if (permissions.data.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center text-center py-12">
        <div className="rounded-full bg-muted p-4 mb-4">
          <ShieldCheck className="h-8 w-8 text-muted-foreground" />
        </div>
        <h3 className="text-lg font-semibold">
          You don't have any permissions yet
        </h3>
        <p className="text-muted-foreground">
          Add a new permission to get started
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
  return (
    <div className="flex flex-col gap-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold tracking-tight">Permissions</h1>
          <p className="text-muted-foreground">
            Manage the permissions that can be granted to roles
          </p>
        </div>
        <AddPermission />
      </div>
      <PermissionsTable />
    </div>
  )
}
