import models
import fields


class ResUsers(models.OdooModel):
    _name = 'res.users'

    login = fields.StringField()
    department_id = fields.Many2oneField()


class Task(models.OdooModel):
    _name = 'lsv.construction.task'

    name = fields.StringField()
    proposal_id = fields.Many2oneField()
    description = fields.Many2oneField()
    project_id = fields.Many2oneField()
    start_date = fields.DateField()
    end_date = fields.DateField()
    employee_ids = fields.Many2manyField()
    machinery_ids = fields.Many2manyField()
    lines_ids = fields.Many2manyField()


# task = Task(
#     id=93,
#     name='name testing 3',
#     proposal_id=10,
#     description='esta es una description de ejemplo',
#     project_id=4,
#     valuation='regular',
#     start_date='2025-12-29',
#     end_date='2025-12-29',
#     employee_ids=[],
#     machinery_ids=[],
#     lines_ids=[],
# )

# task.update()

print(ResUsers.search_read())
