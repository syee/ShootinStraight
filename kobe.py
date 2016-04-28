if chartType == "proportionPoints":
        # REVIESE
        cb.set_label('Relative Frequency of Points')
        cb.set_ticks([0.0, 0.10, 0.20, 0.75, 0.90])
        cb.set_ticklabels(['0%','0.20%', '0.40%','3.0%', '4.0%'])
    elif chartType == "rawPoints":
        # REVIESE
        cb.set_label('Points')
        cb.set_ticks([0.0, 0.10, 0.20, 0.75, 0.90])
        cb.set_ticklabels(['0%','0.10%', '0.20%','1.5%', '2%'])
    elif chartType == "allShots":

        # REVIESE
        cb.set_label('Number of Shots')
        cb.set_ticks([0.0, 0.10, 0.20, 0.75, 0.90])
        cb.set_ticklabels(['0%','0.10%', '0.20%','1.5%', '2%'])
    else:
        cb.set_label('Field Goal Percentage')
        cb.set_ticks([0.0, 0.25, 0.5, 0.75, 1.0])
        cb.set_ticklabels(['0%','25%', '50%','75%', '100%'])
