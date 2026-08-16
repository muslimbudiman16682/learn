import { EllipsisVertical } from "lucide-react"
import { useState } from "react"

import type { PermissionPublic } from "@/client"
import { Button } from "@/components/ui/button"
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"
import DeletePermission from "./DeletePermission"
import EditPermission from "./EditPermission"

interface PermissionActionsMenuProps {
  permission: PermissionPublic
}

export const PermissionActionsMenu = ({
  permission,
}: PermissionActionsMenuProps) => {
  const [open, setOpen] = useState(false)

  return (
    <DropdownMenu open={open} onOpenChange={setOpen}>
      <DropdownMenuTrigger asChild>
        <Button variant="ghost" size="icon">
          <EllipsisVertical />
        </Button>
      </DropdownMenuTrigger>
      <DropdownMenuContent align="end">
        <EditPermission permission={permission} onSuccess={() => setOpen(false)} />
        <DeletePermission id={permission.id} onSuccess={() => setOpen(false)} />
      </DropdownMenuContent>
    </DropdownMenu>
  )
}
