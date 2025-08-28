import asyncio
from agents import Agent, Runner, RunContextWrapper, function_tool
import rich
from pydantic import BaseModel
from connection import config  

#---------------------------------------------------------
# Define StudentProfile model using Pydantic
#---------------------------------------------------------
class StudentProfile(BaseModel):
    student_id: str
    student_name: str
    current_semester: int
    total_courses: int


#---------------------------------------------------------
# Create a StudentProfile instance
#---------------------------------------------------------
student = StudentProfile(
    student_id="STU-456",
    student_name="Hassan Ahmed",
    current_semester=4,
    total_courses=5
)


#---------------------------------------------------------
# Define a function tool to fetch student details
#---------------------------------------------------------
@function_tool
def get_student_info(wrapper: RunContextWrapper[StudentProfile]):
    student = wrapper.context
    return (
        f"🎓 Student Profile\n"
        f"------------------------\n"
        f"🆔 Student ID       : {student.student_id}\n"
        f"👤 Student Name     : {student.student_name}\n"
        f"📚 Current Semester : {student.current_semester}\n"
        f"📖 Total Courses    : {student.total_courses}"
    )


#---------------------------------------------------------
# Create the Agent
#---------------------------------------------------------
student_agent = Agent[StudentProfile](
    name="Student Info Agent",
    instructions="You are a helpful assistant, always call the tool to get student details.",
    tools=[get_student_info]
)


#---------------------------------------------------------
# Define async main function to run the agent
#---------------------------------------------------------
async def main():
    result = await Runner.run(
        starting_agent=student_agent,
        input="Tell me the student profile details",
        run_config=config,
        context=student
    )
    # Print the final output in styled format
    rich.print(result.final_output)


#---------------------------------------------------------
# Entry point of the script
#---------------------------------------------------------
if __name__ == "__main__":
    asyncio.run(main())