import { Briefcase, Home, Shield, ShieldCheck, Users } from "lucide-react"
import { useTranslation } from "react-i18next"

import { SidebarAppearance } from "@/components/Common/Appearance"
import { SidebarLanguageSwitcher } from "@/components/Common/LanguageSwitcher"
import { Logo } from "@/components/Common/Logo"
import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarHeader,
} from "@/components/ui/sidebar"
import useAuth from "@/hooks/useAuth"
import { type Item, Main } from "./Main"
import { User } from "./User"

export function AppSidebar() {
  const { user: currentUser } = useAuth()
  const { t } = useTranslation()

  const baseItems: Item[] = [
    { icon: Home, title: t("sidebar.dashboard"), path: "/" },
    { icon: Briefcase, title: t("sidebar.items"), path: "/items" },
  ]

  const superuserItems: Item[] = [
    { icon: Users, title: t("sidebar.admin"), path: "/admin" },
    { icon: Shield, title: t("sidebar.roles"), path: "/roles" },
    { icon: ShieldCheck, title: t("sidebar.permissions"), path: "/permissions" },
  ]

  const items = currentUser?.is_superuser
    ? [...baseItems, ...superuserItems]
    : baseItems

  return (
    <Sidebar collapsible="icon">
      <SidebarHeader className="px-4 py-6 group-data-[collapsible=icon]:px-0 group-data-[collapsible=icon]:items-center">
        <Logo variant="responsive" />
      </SidebarHeader>
      <SidebarContent>
        <Main items={items} />
      </SidebarContent>
      <SidebarFooter>
        <SidebarLanguageSwitcher />
        <SidebarAppearance />
        <User user={currentUser} />
      </SidebarFooter>
    </Sidebar>
  )
}

export default AppSidebar
