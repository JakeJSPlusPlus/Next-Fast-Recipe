
import Link from "next/link";
import { AnchorHTMLAttributes, ReactNode } from "react";

interface HeaderLinkProps extends AnchorHTMLAttributes<HTMLAnchorElement> {
  children: ReactNode;
  href: string;
}

export function HeaderLink({ children, href, ...props }: HeaderLinkProps) {
  return (
    <Link href={href} {...props} className="flex items-center hover:underline">
      {children}
    </Link>
  );
}
