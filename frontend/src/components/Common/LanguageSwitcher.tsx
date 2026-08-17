import { Languages } from "lucide-react"
import { useTranslation } from "react-i18next"

import {
  changeLanguage,
  type SupportedLanguage,
} from "@/i18n/config"
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"
import {
  SidebarMenuButton,
  SidebarMenuItem,
  useSidebar,
} from "@/components/ui/sidebar"

const LANGUAGE_LABELS: Record<SupportedLanguage, string> = {
  id: "Bahasa Indonesia",
  en: "English",
}

export const SidebarLanguageSwitcher = () => {
  const { isMobile } = useSidebar()
  const { t, i18n } = useTranslation()
  const currentLanguage = i18n.language as SupportedLanguage

  return (
    <SidebarMenuItem>
      <DropdownMenu modal={false}>
        <DropdownMenuTrigger asChild>
          <SidebarMenuButton
            tooltip={t("sidebar.language")}
            data-testid="language-button"
          >
            <Languages className="size-4 text-muted-foreground" />
            <span>{t("sidebar.language")}</span>
          </SidebarMenuButton>
        </DropdownMenuTrigger>
        <DropdownMenuContent
          side={isMobile ? "top" : "right"}
          align="end"
          className="w-(--radix-dropdown-menu-trigger-width) min-w-56"
        >
          <DropdownMenuItem
            data-testid="language-id"
            onClick={() => changeLanguage("id")}
            className={
              currentLanguage === "id" ? "font-semibold" : undefined
            }
          >
            {LANGUAGE_LABELS.id}
          </DropdownMenuItem>
          <DropdownMenuItem
            data-testid="language-en"
            onClick={() => changeLanguage("en")}
            className={
              currentLanguage === "en" ? "font-semibold" : undefined
            }
          >
            {LANGUAGE_LABELS.en}
          </DropdownMenuItem>
        </DropdownMenuContent>
      </DropdownMenu>
    </SidebarMenuItem>
  )
}

export default SidebarLanguageSwitcher
