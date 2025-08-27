import { createFileRoute } from '@tanstack/react-router'

export const Route = createFileRoute('/signup/farmer')({
  component: RouteComponent,
})

function RouteComponent() {
  return <div>Hello "/signup/farmer"!</div>
}
