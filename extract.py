import re
import sys

f = open(sys.argv[1].strip(), "r")
lines = f.readlines()
f.close()


def clean_line(line):
    propose = ""
    oppose = ""
    if "propose" in line or "oppose" in line:
        try:
            propose = re.search("(([A-Z]{2}[0-9]*\/*\s*)+\spropose)", line).groups()[0]
            propose = re.sub("[0-9]+", "", propose)
        except:
            pass
        try:
            oppose = re.search("(([A-Z]{2}[0-9]*\/*\s*)+\soppose)", line).groups()[0]
            oppose = re.sub("[0-9]+", "", oppose)
        except:
            pass
    return [propose, oppose]

def count_countries(pais1, pais2, lines):
    propose_together = 0
    oppose_together = 0
    oppose_each_other = 0

    for line in lines:
        # propose together
        if pais1 in line[0] and pais2 in line[0]:
            propose_together += 1
        elif pais1 in line[1] and pais2 in line[1]:
            oppose_together += 1
        elif pais1 in line[0] and pais2 in line[1]:
            oppose_each_other += 1
        elif pais2 in line[0] and pais1 in line[1]:
            oppose_each_other += 1

    print "Conteo de votos de %s versus %s" % (pais1, pais2,)
    print "propose_together %i" % propose_together
    print "oppose_together %i" % oppose_together
    print "oppose_each_other %i" % oppose_each_other


new_lines = []
chile_se_opone = 0
for line in lines:
    line = re.sub("\s+", " ", line)
    line = line.strip()
    if line.startswith("Article"):
        article_line = line
    if "PE" in line and "CL" in line and "US" in line:
        tmp = clean_line(line)
        if "PE" in tmp[0] and "US" in tmp[0] and "CL" in tmp[1]:
            chile_se_opone = chile_se_opone + 1
            print "* %s" % article_line
            print line
        elif "PE" in tmp[1] and "US" in tmp[1] and "CL" in tmp[0]:
            chile_se_opone = chile_se_opone + 1
            print "* %s" % article_line
            print line
    if line.startswith("["):
        new_lines.append(clean_line(line))

print "Chile se opone a US y PE %i veces" % chile_se_opone


print "Hay %i lineas de informacion" % len(new_lines)
count_countries("PE", "US", new_lines)
print "\n---------------------\n"
count_countries("PE", "CL", new_lines)
print "\n---------------------\n"
count_countries("US", "CL", new_lines)

