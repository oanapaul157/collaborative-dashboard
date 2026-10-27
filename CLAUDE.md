# Collaborative Dashboard

A Trello-like app I'm building **to learn** full-stack development.
See README.md for the stack and how to run it.

## How to help me
- Explain concepts and show one or two examples. Don't write whole features;
  I write the code myself.
- Point out bugs and explain them, but let me fix them unless I ask you to.
- Review my code when I ask: correctness first, then idiomatic style.

## Plan
1. [x] DB layer: settings, SQLAlchemy models, first Alembic migration
2. [x] CRUD API for boards, columns, tasks, split into routers
3. [ ] Auth: register/login, JWT, only members can see a board
4. [ ] Frontend basics: routing, board list, board page with columns and tasks
5. [ ] Drag and drop with @dnd-kit
6. [ ] Members: invite by email, roles
7. [ ] WebSockets: one room per board; server broadcasts "board X changed" after each change

## Decisions
- Frontend fetches all server data through TanStack Query, so step 7 is just
  `queryClient.invalidateQueries(['board', id])` when a WebSocket message arrives.
- Step 2 uses a placeholder `get_current_user` (X-User-Id header), replaced by JWT in step 3.
- Creating a board also creates the owner's BoardMember row (role "owner").
- Columns and tasks are ordered by an integer `position`.
