doctype 5
html ->
  head ->
    meta charset: 'utf-8'
    title "Style Guide"
    link rel: 'stylesheet', type:'text/css', href:'fancy.css'
    script src: "https://ajax.googleapis.com/ajax/libs/jquery/1.4.2/jquery.min.js"
    script src: "https://ajax.googleapis.com/ajax/libs/jqueryui/1.8.16/jquery-ui.min.js"
  coffeescript ->

    # Does this element appear in the nav?
    elem_valid = (elem) ->
      return not (elem.tagName == 'H4' or elem.tagName == 'H1')

    $(document).ready ->
       
      id = 0
      $(":header").each ->
        # Add content to the nav for each header. We also set id attributes of
        # the headers and the nav items such that if you know one you can
        # access the other. This is helpful for doing the coloring.
        return if not elem_valid(this)
        id += 1

        elem = $(this)
        elem.attr("id", "#{id}")
        new_link = $("<div class='nav-items' id='nav-item-#{id}'><a href='javascript:void(0)' class='sidebar-content #{"sidebar-indent" if this.tagName == 'H3'}'>#{this.innerHTML}</a></div>")
        $("#sidebar").append(new_link)

        new_link.click ->
          #scroll to relevant header
          $('html, body').animate(scrollTop : elem.offset().top, 1000)

      #TODO last_best blalbla

      last_best = undefined

      $(window).scroll ->
        # Every time the window scrolls, potentially update the highlight on
        # the nav to the new focused section.
        best = 999999999
        best_header = undefined

        $(":header").each ->
          return if not elem_valid this

          dist = ($(window).scrollTop() - $(this).offset().top)
          if dist >= 0 and dist < best
            best = dist
            best_header = $(this)

        # I check innerHTML as a fairly hacky sort if equality since testing
        # nodes for absolute equality is fairly difficult.
        if best_header and ((not last_best) or (best_header[0].innerHTML != last_best[0].innerHTML))
          last_best = best_header
          id = best_header.attr('id')
          $("#nav-item-#{id}").animate({backgroundColor: '#eee'}, 'slow')

        $(".nav-items").each ->
          return if this.id == "nav-item-" + best_header.attr('id')
          $(this).stop()
          $(this).css('backgroundColor', '#fff')


  body ->
    div id: "sidebar", ->
      div id: "sidebar-header", -> "Navigation"
    div id: "everything-else", ->
      @content
