import * as React from "react";

// The shared input primitive. forwardRef + {...props} is how a design-system
// primitive is supposed to look: the caller controls type, id, aria-*, and
// the ref reaches the DOM node so form libraries can register it.
export const Input = React.forwardRef<
  HTMLInputElement,
  React.InputHTMLAttributes<HTMLInputElement>
>(({ className, ...props }, ref) => (
  <input ref={ref} className={cn(base, className)} {...props} />
));
Input.displayName = "Input";
