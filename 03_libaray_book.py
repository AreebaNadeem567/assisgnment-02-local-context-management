import asyncio
from agents import Agent, Runner, function_tool, RunContextWrapper
from pydantic import BaseModel
from connection import config
import rich

#---------------------------------------------------------
# Define LibraryBook model using Pydantic
#---------------------------------------------------------
class LibraryBook(BaseModel):
    book_id: str
    book_title: str
    author_name: str
    is_available: bool


#---------------------------------------------------------
# Create a LibraryBook instance
#---------------------------------------------------------
library_book = LibraryBook(
    book_id="BOOK-123",
    book_title="Python Programming",
    author_name="John Smith",
    is_available=True
)

#---------------------------------------------------------
# Define a tool function to fetch book information
#---------------------------------------------------------
@function_tool
def get_book_info(wrapper: RunContextWrapper[LibraryBook]):
    book = wrapper.context
    return (
        f"📚 Book Details\n"
        f"------------------------\n"
        f"🔢 Book ID    : {book.book_id}\n"
        f"📖 Title      : {book.book_title}\n"
        f"✍️ Author     : {book.author_name}\n"
        f"🟢 Status     : {book.is_available}"
    )


#---------------------------------------------------------
# Create the Agent to fetch book info
#---------------------------------------------------------
book_agent = Agent[LibraryBook](
    name="Library Book Agent",
    instructions="You are a helpful assistant, always call the tool to get library book details.",
    tools=[get_book_info]
)


#---------------------------------------------------------
# Define async main function to run the agent
#---------------------------------------------------------
async def main():
    result = await Runner.run(
        starting_agent=book_agent,
        input="Give me the details of the book",
        run_config=config,
        context=library_book
    )
    rich.print(result.final_output)


#---------------------------------------------------------
# Entry point of the script
#---------------------------------------------------------
if __name__ == "__main__":
    asyncio.run(main())
