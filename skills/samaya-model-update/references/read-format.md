# The Read written on the sheet

Moved out of `SKILL.md` to keep it lean; read it before writing the Read.

## THE READ — a written answer on the sheet, not only in chat

The written summary below goes in chat, and chat is not where the workbook lives. Anyone opening
the file next week — the analyst, a colleague, the MD who asked for it — sees cells, not the
conversation that produced them. So the roll also writes a **Read** into the workbook itself.

**Where it goes.** A `Roll notes` block at the top of the change tracker, or in the first rows of
the sheet carrying the change log, merged across the table width, wrapped, prose.

**What it carries.** Two or three sentences of prose — the period closed and the roll mode, how
the print came in against what the model previously held at the lines that moved most, and what
moved in the forecast and on whose basis — then **three labelled groups**, per the attention
classification above. Every line in every group is a live internal hyperlink to the cell it
refers to, so the analyst clicks the sentence and lands on the number:

- **Reported — settled.** The actuals entered, by line. No fill, each linked to its source Note.
  The analyst can skip this group: these are what the company said, and there is nothing to
  question. Say how many lines it covers and move on rather than listing all of them.
- **Estimates to review.** Forecast lines the roll moved or left standing where the new period
  gives reason to look again: where the estimate now sits against the new guidance, against what
  the analyst previously modelled, and against consensus where a provider was declared. One line
  each, naming which of the three prompted the flag. These carry the attention fill.
- **Mechanics to check.** Formulas, references and structural items worth a second look — a
  hardcode in a row of formulas, a reference re-pointed after an insertion, an aggregate range
  widened, an identity that ties only on rounding. These carry the attention fill.

Then one closing sentence on what could not be sourced and what still waits on the analyst.

The point of the three groups is that the analyst's attention is the scarce thing. A roll that
returns eighty changed cells undifferentiated has moved the work rather than done it; a roll that
says "sixty of these are reported and settled, six estimates want your view, two formulas want a
look" has done it.

Written last, from the change tracker only. No cell references in the prose — name the lines in
words. It describes what the roll did; it states no rating, target or recommendation.

The chat summary and the sheet Read say the same things at different lengths. Where only one can
be written, it is the sheet Read, because it survives the session.
