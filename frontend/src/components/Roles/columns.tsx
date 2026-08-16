import type { ColumnDef } from "@tanstack/react-table"

import type { RolePublic } from "@/client"
import { Badge } from "@/components/ui/badge"
import { cn } from "@/lib/utils"
import { RoleActionsMenu } from "./RoleActionsMenu"

export const columns: ColumnDef<RolePublic>[] = [
  {
    accessorKey: "name",
    header: "Name",
    cell: ({ row }) => (
      <span className="font-medium">{row.original.name}</span>
    ),
  },
  {
    accessorKey: "description",
    header: "Description",
    cell: ({ row }) => {
      const description = row.original.description
      return (
        <span
          className={cn(
            "max-w-xs truncate block text-muted-foreground",
            !description && "italic",
          )}
        >
          {description || "No description"}
        </span>
      )
    },
  },
  {
    id: "permissions",
    header: "Permissions",
    cell: ({ row }) => {
      const count = row.original.permissions?.length ?? 0
      return (
        <Badge variant={count > 0 ? "secondary" : "outline"}>
          {count} {count === 1 ? "permission" : "permissions"}
        </Badge>
      )
    },
  },
  {
    id: "actions",
    header: () => <span className="sr-only">Actions</span>,
    cell: ({ row }) => (
      <div className="flex justify-end">
        <RoleActionsMenu role={row.original} />
      </div>
    ),
  },
]
