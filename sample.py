def generate_bins_advanced(shot_df, gridNum, chartType):
    x = shot_df.LOC_X[shot_df['LOC_Y']<425.1] #i want to make sure to only include shots I can draw
    y = shot_df.LOC_Y[shot_df['LOC_Y']<425.1]

    x_made = shot_df.LOC_X[(shot_df['SHOT_MADE_FLAG']==1) & (shot_df['LOC_Y']<425.1)]
    y_made = shot_df.LOC_Y[(shot_df['SHOT_MADE_FLAG']==1) & (shot_df['LOC_Y']<425.1)]

    #compute number of shots made and taken from each hexbin location
    hb_shot = plt.hexbin(x, y, gridsize=gridNum, extent=(-250,250,425,-50));
    plt.close() #don't want to show this figure!
    hb_made = plt.hexbin(x_made, y_made, gridsize=gridNum, extent=(-250,250,425,-50),cmap='PuRd_r');
    plt.close()

    # Calculate total points
    if chartType == "allShots":
        shootingBins = hb.shot.get_array()
    if chartType == "fieldGoal":
        shootingBins = hb_made.get_array() / hb.shot.get_array()
    if chartType == "proportionPoints":
        points = calculateTotalPointsFromField(shot_df)
        shootingBins = hb_made.get_array() / points
    if chartType == "rawPoints":
        shootingBins = hb_made.get_array()

    #compute shooting percentage
    shootingBins[numpy.isnan(shootingBins)] = 0 #makes 0/0s=0

    zCords = []
    max = 0
    # For finding shot groupings
    # workbookNew = xlwt.Workbook()
    # sheetNew = workbookNew.add_sheet("Sheet_1")
    x = 0
    for row in shootingBins:
        zCords.append(row)
        # sheetNew.write(x, 0, row)
        x = x + 1
        if row > max:
            max = row
    # workbookNew.save('percentages.xls')
    hb_made.set_antialiased(False)
    # hb_made.set_color('k')

    return (shootingBins, hb_shot, zCords, hb_made)