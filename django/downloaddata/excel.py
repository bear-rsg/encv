import xlsxwriter
import os
import glob
import time
from education import models as education_models
from health import models as health_models


def write_data_to_worksheet(workbook, worksheet, datamatrix, column_titles=None):
    """
    Writes provided datamatrix to the provided xlsxwriter worksheet
    Provided datamatrix must be a matrix (aka list of list, 2D list)
    A list of column titles can be provided.
    """

    # If column headers written to row 0 this value will increase to 1, as data must not also be written on row 0
    column_titles_adjustment = 0
    column_max_widths = []
    column_titles_style = workbook.add_format({'bold': True, 'font_color': 'white', 'bg_color': '#002060'})

    # Allow for line breaks by setting text_wrap to True
    row_format = workbook.add_format({'text_wrap': True,})

    for row, dataitem in enumerate(datamatrix):

        # Column titles to first row, if provided
        if row == 0 and column_titles:
            for col, title in enumerate(column_titles):
                # Print column titles
                worksheet.write(row, col, title, column_titles_style)
                column_max_widths.append(len(str(title)))  # add initial values to column_max_widths list
            column_titles_adjustment = 1

        # Datamatrix
        for col, value in enumerate(dataitem):
            # Write data for each row
            worksheet.write(row + column_titles_adjustment, col, value, row_format)

            # Determine column widths
            col_width = len(str(value))
            # Set initial values in column_max_widths list, if not set in columns above
            if len(column_max_widths) <= col:
                column_max_widths.append(col_width)
            # Overwrite values in column_max_widths list if greater than them
            elif column_max_widths[col] < col_width:
                column_max_widths[col] = col_width

    # Set the column widths
    for col, cmw in enumerate(column_max_widths):
        worksheet.set_column(col, col, cmw)


def media_url_full(request, file_url):
    return f"{request.scheme}://{request.META['HTTP_HOST']}{file_url}"


def create_workbook(request):
    """
    Creates a spreadsheet and returns its file path
    """

    # Delete all existing files in the data folder
    data_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
    files = glob.glob(data_path + '/*')
    for f in files:
        os.remove(f)

    # Establish new file name
    file_name = f'encv_data_{time.strftime("%Y-%m-%d_%H-%M")}.xlsx'
    file_path = os.path.join(data_path, file_name)

    # Create workbook
    workbook = xlsxwriter.Workbook(file_path)

    # Create worksheet 1: Education - Journal Entries
    columns_journal_entries = [
        "ID",
        "Author",
        "Prompt",
        "Text",
        "Link",
        "Image (download link)",
        "Audio (download link)",
        "Video (download link)",
        "Created",
        "Last Updated"
    ]
    data_journal_entries = []
    for journal_entry in education_models.JournalEntry.objects.all().select_related('author',).prefetch_related('prompt'):
        data_journal_entries.append([
            journal_entry.id,
            str(journal_entry.author),
            journal_entry.prompts_as_str,
            journal_entry.text,
            journal_entry.link,
            media_url_full(request, journal_entry.image.url) if journal_entry.image else None,
            media_url_full(request, journal_entry.audio.url) if journal_entry.audio else None,
            media_url_full(request, journal_entry.video.url) if journal_entry.video else None,
            str(journal_entry.created)[:16],
            str(journal_entry.last_updated)[:16],
        ])
    write_data_to_worksheet(
        workbook,
        workbook.add_worksheet("Education - Journal Entries"),
        data_journal_entries,
        columns_journal_entries
    )

    # Create worksheet 2: Health - Conversations
    columns_conversations = [
        "ID",
        "Author",
        "Conversation Date",
        "Conversation Audio (download link)",
        "Conversation Transcript (download link)",
        "Cancer Champion Reflection",
        "Created",
        "Last Updated"
    ]
    data_conversations = []
    for conversation in health_models.Conversation.objects.all().select_related('author',):
        data_conversations.append([
            conversation.id,
            str(conversation.author),
            str(conversation.conversation_date)[:10],
            media_url_full(request, conversation.conversation_audio.url) if conversation.conversation_audio else None,
            media_url_full(request, conversation.conversation_transcript.url) if conversation.conversation_transcript else None,
            conversation.cancer_champion_reflection,
            str(conversation.created)[:16],
            str(conversation.last_updated)[:16],
        ])
    write_data_to_worksheet(
        workbook,
        workbook.add_worksheet("Health - Conversations"),
        data_conversations,
        columns_conversations
    )

    # Close workbook and return its file path
    workbook.close()
    return file_path
