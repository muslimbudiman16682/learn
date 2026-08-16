import { useSuspenseQuery } from "@tanstack/react-query"
import { createFileRoute, redirect } from "@tanstack/react-router"
import { Shield } from "lucide-react"
import { Suspense } from "react"

import { RolesService, UsersService } from "@/client"
import { DataTable } from "@/components/Common/DataTable"
import PendingRoles from "@/components/Pending/PendingRoles"
import AddRole from "@/components/Roles/AddRole"
import { columns } from "@/components/Roles/columns"

function getRolesQueryOptions() {
  return {
    queryFn: async () =>
      (await RolesService.readRoles({ query: { skip: 0, limit: 100 } })).data,
    queryKey: ["roles"],
  }
}

export const Route = createFileRoute("/_layout/roles")({
  component: Roles,
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
        title: "Roles - FastAPI Template",
      },
    ],
  }),
})

function RolesTableContent() {
  const { data: roles } = useSuspenseQuery(getRolesQueryOptions())

  if (roles.data.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center text-center py-12">
        <div className="rounded-full bg-muted p-4 mb-4">
          <Shield className="h-8 w-8 text-muted-foreground" />
        </div>
        <h3 className="text-lg font-semibold">You don't have any roles yet</h3>
        <p className="text-muted-foreground">Add a new role to get started</p>
      </div>
    )
  }

  return <DataTable columns={columns} data={roles.data} />
}

function RolesTable() {
  return (
    <Suspense fallback={<PendingRoles />}>
      <RolesTableContent />
    </Suspense>
  )
}

function Roles() {
  return (
    <div className="flex flex-col gap-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold tracking-tight">Roles</h1>
          <p className="text-muted-foreground">
            Create roles and control which permissions they grant
          </p>
        </div>
        <AddRole />
      </div>
      <RolesTable />
    </div>
  )
}
