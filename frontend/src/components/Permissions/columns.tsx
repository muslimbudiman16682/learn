import type { ColumnDef } from "@tanstack/react-table"

import type { PermissionPublic } from "@/client"
import { cn } from "@/lib/utils"
import { PermissionActionsMenu } from "./PermissionActionsMenu"

export const columns: ColumnDef<PermissionPublic>[] = [
  {
    accessorKey: "code",
    header: "Code",
    cell: ({ row }) => (
      <span className="font-mono text-sm font-medium">
        {row.original.code}
      </span>
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
    id: "actions",
    header: () => <span className="sr-only">Actions</span>,
    cell: ({ row }) => (
      <div className="flex justify-end">
        <PermissionActionsMenu permission={row.original} />
      </div>
    ),
  },
]
