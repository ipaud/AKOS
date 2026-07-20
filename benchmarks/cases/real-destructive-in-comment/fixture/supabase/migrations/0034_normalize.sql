-- Shape from a real repository: planned technical debt, recorded in a comment.
--
--   PLANNED DEBT: once the new bundle has a week in production, a later
--   migration must do
--     alter table availability_requests drop column "date";
--     drop function availability_sync_legacy_date() cascade;
--
create table availability_slots (
  id uuid primary key,
  request_id uuid not null
);
