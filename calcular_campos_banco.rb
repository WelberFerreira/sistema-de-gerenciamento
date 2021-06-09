    unless attributes[:quesito21].blank? || attributes[:quesito22].blank? || attributes[:quesito23].blank?
       nota = Bucket.where(id: @bucket)
      .pluck(:quesito21,:quesito22, :quesito23)
      .map(&:sum)
      .sum
       
    end
