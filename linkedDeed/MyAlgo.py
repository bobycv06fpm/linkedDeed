"""Implementing an algorithm to find out the best match jobs."""
import csv
import sqlite3
import unicodedata

global total_count

text = []
labels = []
filename = 'SkillsetUniversal.txt'


def read_txt(file, text):
    """Reading data from text files(universal skill list)."""
    with open(file, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            for item in row:
                text.append(item)
    return text


def select_from():
    """Reading data from tables."""
    conn = sqlite3.connect('stuffToPlot.db')
    c = conn.cursor()
    jobs = []
    for row in c.execute('SELECT DESCRIPTION FROM stuf'):
        jobs.append(row)
    c.close()
    c = conn.cursor()
    skills = []
    for row in c.execute('SELECT description FROM stuffToPlot'):
        skills.append(row)
    c.close()
    conn.close()
    return jobs, skills


def jobs_calc(job, text):
    """Calculate how many skills match."""
    temp = 0
    for uni_word in text:
        if uni_word in job:
            temp += 1
    return temp


def data_cleanup(jobs, skills, txt):
    """Clean up of each job description and skills."""
    for i in range(len(jobs)):
        jobs[i] = unicodedata.normalize('NFKD', "".join(jobs[i]).replace('\n', ' ').replace('\t', ' ')).encode('ascii','ignore')

    # cz skills will just be in 1 cell
    skills[0] = unicodedata.normalize('NFKD', "".join(skills[0])).encode('ascii', 'ignore')
    skill_l = (skills[0].split(', '))
    skill_list = [item.lower() for item in skill_l]
    text = [item.lower() for item in txt]
    jobss = [item.lower() for item in jobs]
    job_list = []
    for job in jobss:
        job_list.append(job.split(' '))
    return skill_list, text, job_list


def accuracy(skill_list, text, job_list):
    """Calculate match accuracy for each job."""
    # skills_required = []
    # skills_match = []
    match = []  # match depending upon the skills required.
    for job in job_list:
        x = jobs_calc(job, text)
        y = jobs_calc(job, skill_list)
        # skills_required.append(x)
        # skills_match.append(y)
        match.append((float(y) / x) * 100)
    return match


def update_table(match):
    """Update it in sqlite and order this in desc."""
    conn = sqlite3.connect('stuffToPlot.db')
    sql = '''UPDATE stuf SET match = ? WHERE id = ?'''
    for i in range(len(match)):
        cur = conn.cursor()
        cur.execute(sql, match[i], i + 1)
        conn.commit()
        cur.close()
    conn.close()

txt = read_txt(filename, labels)
jobs, skills = select_from()
skill_list, text, job_list = data_cleanup(jobs, skills, txt)
skills_you_have = jobs_calc(skill_list, text)

match = accuracy(skill_list, text, job_list)
update_table(match)