import type { ColumnDef } from "@tanstack/react-table"
import type { TFunction } from "i18next"

import type { PermissionPublic } from "@/client"
import { cn } from "@/lib/utils"
import { PermissionActionsMenu } from "./PermissionActionsMenu"

export const getColumns = (t: TFunction): ColumnDef<PermissionPublic>[] => [
  {
    accessorKey: "code",
    header: t("permissions.columns.code"),
    cell: ({ row }) => (
      <span className="font-mono text-sm font-medium">
        {row.original.code}
      </span>
    ),
  },
  {
    accessorKey: "description",
    header: t("permissions.columns.description"),
    cell: ({ row }) => {
      const description = row.original.description
      return (
        <span
          className={cn(
            "max-w-xs truncate block text-muted-foreground",
            !description && "italic",
          )}
        >
          {description || t("permissions.columns.noDescription")}
        </span>
      )
    },
  },
  {
    id: "actions",
    header: () => <span className="sr-only">{t("common.actions")}</span>,
    cell: ({ row }) => (
      <div className="flex justify-end">
        <PermissionActionsMenu permission={row.original} />
      </div>
    ),
  },
]
