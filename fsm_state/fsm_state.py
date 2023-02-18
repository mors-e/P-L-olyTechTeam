from aiogram.dispatcher.filters.state import State, StatesGroup


class FSMFillForm(StatesGroup):
    email = State()
    FIO_user = State()
    division = State()
    FIO_leader = State()
    date_start_working = State()
    rate_expectations = State()
    full_expectations = State()
    college_revue = State()
    college_revue_more = State()
    college_intimate = State()
    college_other = State()
    your_duties = State()
    leader_task = State()
    leader_task_solve = State()
    tasks_hard = State()
    address_colleagues_questions = State()
    address_leader_questions = State()
    helping_questions = State()
    leader_feedback = State()
    tutor = State()
    launch = State()
    launch_people = State()
    contact_colleagues = State()
    sick = State()
    income = State()
    holiday = State()
    structure_company = State()
    operations_divisions = State()
    covering_divisions = State()
    subordinate_institutions = State()
    working_comfort = State()
    comfort = State()
    other = State()


class FSMChatStaff(StatesGroup):
    start = State()
    chat_hr = State()
    questions = State()
    await_message = State()


class FSMChatHR(StatesGroup):
    start = State()
    request = State()
    await_message = State()
