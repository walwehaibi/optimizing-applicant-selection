# optimizing-applicant-selection
Optimizing the selection of applicants for two independent organizations from the same pool of applicants

## Problem description:
Los Angeles Homeless Services Authority (LAHSA) and Safe Parking LA (SPLA) are two organizations in Los Angeles that service the homeless community. LAHSA provides beds in shelters and SPLA manages spaces in parking lots for people living in their cars. In the city’s new app for homelessness, people in need of housing can apply for a space with either service. This program will help SPLA choose applicants that meet the SPLA specific requirements for the space and that also optimize the use of the parking lot for that week.

SPLA requirements differ from LAHSA. They are both picking from the same applicant list. They each have different resources and may not be qualified to accept the same applicants. SPLA and LAHSA alternate choosing applicants one by one. They must choose an applicant if there is still a qualified one on the list (no passing). SPLA applicants must have a car and driver’s license, but no medical conditions. LAHSA shelter can only serve women over 17 years old without pets. Both SPLA and LAHSA have limited resources that must be used efficiently. Efficiency is calculated by how many of the spaces are used during the week. For example, a SPLA parking lot has 10 spaces and can have at most 10*7 days = 70 different applicants for the week. SPLA tries to maximize its efficiency rate.

## Input file:
The file input.txt is formatted as follows:
  - First line: strictly positive 32-bit integer b, number of beds in the shelter, b <= 40.
  - Second line: strictly positive 32-bit integer p, the number of spaces in the parking lot
  - Third line: strictly positive 32-bit integer L, number of applicants chosen by LAHSA so far.
  - Next L lines: L number of Applicant ID (5 digits) , separated with the End-of-line character LF.
  - Next line: strictly positive 32-bit integer S, number of applicants chosen by SPLA so far. Next S lines: S number of Applicant ID (5 digits), separated with the End-of-line character LF.
  - Next line: strictly positive 32-bit integer A, total number of applicants
  - Next A lines: the list of A applicant information, separated with the End-of-line character LF.

## Output file:
The file output.txt is formatted as follows: Next applicant chosen by SPLA: Applicant ID (5 digits).


#### Note:
This program was done as part of a coursework, the problem presented is not real.
