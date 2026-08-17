import type { ColumnDef } from "@tanstack/react-table"
import type { TFunction } from "i18next"

import type { RolePublic } from "@/client"
import { Badge } from "@/components/ui/badge"
import { cn } from "@/lib/utils"
import { RoleActionsMenu } from "./RoleActionsMenu"

export const getColumns = (t: TFunction): ColumnDef<RolePublic>[] => [
  {
    accessorKey: "name",
    header: t("roles.columns.name"),
    cell: ({ row }) => (
      <span className="font-medium">{row.original.name}</span>
    ),
  },
  {
    accessorKey: "description",
    header: t("roles.columns.description"),
    cell: ({ row }) => {
      const description = row.original.description
      return (
        <span
          className={cn(
            "max-w-xs truncate block text-muted-foreground",
            !description && "italic",
          )}
        >
          {description || t("roles.columns.noDescription")}
        </span>
      )
    },
  },
  {
    id: "permissions",
    header: t("roles.columns.permissions"),
    cell: ({ row }) => {
      const count = row.original.permissions?.length ?? 0
      return (
        <Badge variant={count > 0 ? "secondary" : "outline"}>
          {t("roles.columns.permissionCount", { count })}
        </Badge>
      )
    },
  },
  {
    id: "actions",
    header: () => <span className="sr-only">{t("common.actions")}</span>,
    cell: ({ row }) => (
      <div className="flex justify-end">
        <RoleActionsMenu role={row.original} />
      </div>
    ),
  },
]
