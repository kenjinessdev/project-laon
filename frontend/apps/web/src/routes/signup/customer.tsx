import { createFileRoute } from '@tanstack/react-router'

export const Route = createFileRoute('/signup/customer')({
  component: RouteComponent,
})

function RouteComponent() {
  return <div>Hello "/signup/customer"!</div>
}
