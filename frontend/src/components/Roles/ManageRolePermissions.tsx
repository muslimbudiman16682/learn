import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import { ShieldCheck } from "lucide-react"
import { useState } from "react"
import { useTranslation } from "react-i18next"

import { PermissionsService, type RolePublic, RolesService } from "@/client"
import { Button } from "@/components/ui/button"
import { Checkbox } from "@/components/ui/checkbox"
import {
  Dialog,
  DialogClose,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog"
import { DropdownMenuItem } from "@/components/ui/dropdown-menu"
import { Label } from "@/components/ui/label"
import { LoadingButton } from "@/components/ui/loading-button"
import useCustomToast from "@/hooks/useCustomToast"
import { handleError } from "@/utils"

interface ManageRolePermissionsProps {
  role: RolePublic
  onSuccess: () => void
}

const ManageRolePermissions = ({
  role,
  onSuccess,
}: ManageRolePermissionsProps) => {
  const { t } = useTranslation()
  const [isOpen, setIsOpen] = useState(false)
  const [selectedIds, setSelectedIds] = useState<Set<string>>(
    () => new Set((role.permissions ?? []).map((p) => p.id)),
  )
  const queryClient = useQueryClient()
  const { showSuccessToast, showErrorToast } = useCustomToast()

  const { data: permissions, isPending } = useQuery({
    queryKey: ["permissions"],
    queryFn: async () =>
      (
        await PermissionsService.readPermissions({
          query: { skip: 0, limit: 100 },
        })
      ).data,
    enabled: isOpen,
  })

  const handleOpenChange = (open: boolean) => {
    if (open) {
      setSelectedIds(new Set((role.permissions ?? []).map((p) => p.id)))
    }
    setIsOpen(open)
  }

  const toggle = (id: string) => {
    setSelectedIds((prev) => {
      const next = new Set(prev)
      if (next.has(id)) {
        next.delete(id)
      } else {
        next.add(id)
      }
      return next
    })
  }

  const mutation = useMutation({
    mutationFn: () =>
      RolesService.assignRolePermissions({
        path: { role_id: role.id },
        body: { permission_ids: Array.from(selectedIds) },
      }),
    onSuccess: () => {
      showSuccessToast(t("roles.toast.permissionsUpdated"))
      setIsOpen(false)
      onSuccess()
    },
    onError: handleError.bind(showErrorToast),
    onSettled: () => {
      queryClient.invalidateQueries({ queryKey: ["roles"] })
    },
  })

  return (
    <Dialog open={isOpen} onOpenChange={handleOpenChange}>
      <DropdownMenuItem
        onSelect={(e) => e.preventDefault()}
        onClick={() => handleOpenChange(true)}
      >
        <ShieldCheck />
        {t("roles.managePermissions.menuLabel")}
      </DropdownMenuItem>
      <DialogContent className="sm:max-w-md">
        <DialogHeader>
          <DialogTitle>{t("roles.managePermissions.title")}</DialogTitle>
          <DialogDescription>
            {t("roles.managePermissions.description", { name: role.name })}
          </DialogDescription>
        </DialogHeader>

        <div className="max-h-80 overflow-y-auto py-2">
          {isPending && (
            <p className="text-sm text-muted-foreground">
              {t("roles.managePermissions.loading")}
            </p>
          )}
          {!isPending && permissions?.data.length === 0 && (
            <p className="text-sm text-muted-foreground">
              {t("roles.managePermissions.empty")}
            </p>
          )}
          <div className="flex flex-col gap-3">
            {permissions?.data.map((permission) => (
              <div key={permission.id} className="flex items-start gap-2">
                <Checkbox
                  id={`permission-${permission.id}`}
                  checked={selectedIds.has(permission.id)}
                  onCheckedChange={() => toggle(permission.id)}
                />
                <Label
                  htmlFor={`permission-${permission.id}`}
                  className="flex flex-col gap-0.5 font-normal cursor-pointer"
                >
                  <span className="font-mono text-sm font-medium">
                    {permission.code}
                  </span>
                  {permission.description && (
                    <span className="text-xs text-muted-foreground">
                      {permission.description}
                    </span>
                  )}
                </Label>
              </div>
            ))}
          </div>
        </div>

        <DialogFooter>
          <DialogClose asChild>
            <Button variant="outline" disabled={mutation.isPending}>
              {t("common.cancel")}
            </Button>
          </DialogClose>
          <LoadingButton
            type="button"
            loading={mutation.isPending}
            onClick={() => mutation.mutate()}
          >
            {t("common.save")}
          </LoadingButton>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  )
}

export default ManageRolePermissions
